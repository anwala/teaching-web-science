import sys
import time

from bs4 import BeautifulSoup
from NwalaTextUtils.textutils import genericErrorInfo
from NwalaTextUtils.textutils import getLinks

from playwright.sync_api import sync_playwright
from urllib.parse import quote_plus

from util import paral_rehydrate_tweets
from util import rehydrate_tweet
from util import write_tweets_to_jsonl_file

def is_twitter_user_auth(links, cur_page_uri):

    if( cur_page_uri.strip().startswith('https://twitter.com/home') ):
        return True

    logged_in_links = ['https://twitter.com/home', 'https://t.co/']

    for l in links:
        for log_l in logged_in_links:
            if( l['link'].startswith(log_l) ):
                return True
    return False

def scroll_up(page):
    page.evaluate("window.scrollTo( {'top': 0, 'left': 0, 'behavior': 'smooth'} );")

def scroll_down(page):
    page.evaluate("window.scrollTo( {'top': document.body.scrollHeight, 'left': 0, 'behavior': 'smooth'} );")

def post_tweet(page, msg, button_name='Post'):
    #Post, Reply
    eval_str = f''' document.querySelectorAll('[aria-label="{button_name}"]')[0].click(); '''
    page.evaluate(eval_str)
    time.sleep(1)
    page.keyboard.type(msg, delay=20)
    page.evaluate(''' document.querySelectorAll('[data-testid="tweetButton"]')[0].click(); ''')

    
def color_tweet(page, tweet_link):

    query_slc = f'''article = document.querySelectorAll('[href="{tweet_link}"]');'''
    page.evaluate(query_slc + '''
        if( article.length != 0 )
        {
            article = article[0];
            article.style.backgroundColor = 'red';
            i = 0;
            while(i < 1000)
            {
                if( article.nodeName == 'ARTICLE' )
                {
                    article.style.outline = "thick solid red";
                    article.className = "cust-tweet";
                    break;
                }
                article = article.parentElement;
                i++;
            }
        }
    ''')


def get_tweet_ids_user_timeline_page(screen_name, page, max_tweets):

    empty_result_count = 0
    prev_len = 0
    tweets = []
    tweet_links = set()
    tweet_dets = {}
    break_flag = False

    while( True ):

        page_html = page.content()
        soup = BeautifulSoup(page_html, 'html.parser')
        articles = soup.find_all('article')        

        for i in range(len(articles)):
            
            t = articles[i]
            is_retweet = t.find('span', {'data-testid': 'socialContext'})
            is_retweet = False if is_retweet is None else is_retweet.text.strip().lower().endswith(' retweeted')
            
            tweet_datetime = ''
            tweet_link = t.find('time')
            
            if( tweet_link is None ):
                tweet_link = ''  
            else:
                tweet_datetime = tweet_link.get('datetime', '')
                tweet_link = tweet_link.parent.get('href', '')

            if( tweet_link == '' ):
                continue


            if( screen_name != '' and is_retweet is False and tweet_link.startswith(f'/{screen_name}/') is False ):
                #This tweet was authored by someone else, NOT the owner of the timeline, and since it was not retweeted
                continue

            #color_tweet(page, tweet_link)
            tweet_dets[tweet_link] = {'datetime': tweet_datetime, 'is_retweet': is_retweet}
            tweet_links.add( tweet_link )

            print( '\textracted {} tweets'.format(len(tweet_links)) )
            if( len(tweet_links) == max_tweets ):
                break_flag = True
                print(f'breaking reached ({len(tweet_links)}) maximum: {max_tweets}')
                break
        
        if( break_flag is True ):
            break

        empty_result_count = empty_result_count + 1 if prev_len == len(tweet_links) else 0
        if( empty_result_count > 5 ):
            print(f'No new tweets found, so breaking')
            break

        prev_len = len(tweet_links)
        print('\tscrolling, then sleeping for 1 second\n')
        scroll_down(page)
        time.sleep(1)


    for tlink in tweet_links:

        stat_screen_name, tid = tlink.split('/status/')
        twt_uri_dets = {
            'tid': tid,
            'status_screen_name': stat_screen_name[1:],
            'datetime': tweet_dets[tlink]['datetime']
        }
        twt_uri_dets['notes'] = {'timeline_screen_name': screen_name, 'is_retweet': tweet_dets[tlink]['is_retweet']}
        tweets.append(twt_uri_dets)
        

    tweets = sorted(tweets, key=lambda x:x['tid'])
    return tweets

def get_timeline_tweets(browser_dets, screen_name, max_tweets=20):

    screen_name = screen_name.strip()
    if( max_tweets < 0  or len(browser_dets) == 0 or screen_name == '' ):
        return {}

    print( f'\nget_timeline_tweets(): {screen_name}' )
    uri = f'https://twitter.com/{screen_name}/with_replies'
    
    payload = {'self': uri, 'tweets': []}
    browser_dets['page'].goto(uri)

    tweet_ids = get_tweet_ids_user_timeline_page( screen_name, browser_dets['page'], max_tweets )
    payload['tweets'] = paral_rehydrate_tweets(tweet_ids)

    return payload

def get_search_tweets(browser_dets, query, max_tweets=20):

    query = query.strip()
    if( max_tweets < 0  or len(browser_dets) == 0 or query == '' ):
        return {}

    print('\nget_timeline_tweets():')
    uri = 'https://twitter.com/search?q=' + quote_plus(query) + '&f=live&src=typd'
    
    payload = {'self': uri, 'tweets': []}
    browser_dets['page'].goto(uri)
    
    tweet_ids = get_tweet_ids_user_timeline_page( '', browser_dets['page'], max_tweets )
    payload['tweets'] = paral_rehydrate_tweets(tweet_ids)

    return payload
    
def get_auth_twitter_pg(playwright, callback_uri=''):
    
    print('\nget_auth_twitter_pg()')

    chromium = playwright.firefox #"chromium" or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    sleep_seconds = 3
    page.goto('https://twitter.com/login')
    
    while( True ):

        print(f'\twaiting for login, sleeping for {sleep_seconds} seconds')
        
        time.sleep(sleep_seconds)
        page_html = page.content()
        page_links = getLinks(uri='', html=page_html, fromMainTextFlag=False)
        scroll_down(page)

        if( is_twitter_user_auth(page_links, page.url) ):
            
            print('\tauthenticated')
            if( callback_uri != '' ):
                page.goto(callback_uri)
                print(f'\tauthenticated, loaded {callback_uri}, sleeping for 3 seconds')
                time.sleep(3)

            
            return {
                'page': page,
                'context': context,
                'browser': browser
            }
    
    return {}

def main():
    
    with sync_playwright() as playwright:
        
        browser_dets = get_auth_twitter_pg(playwright)
        if( len(browser_dets) == 0 ):
            return

        tweets = get_timeline_tweets(browser_dets, 'bllin001', max_tweets=600)
        #tweets = get_search_tweets(browser_dets, 'william & mary', max_tweets=20)
        #write_tweets_to_jsonl_file('acnwala_timeline.json.gz', tweets['tweets'])
        

        #post_tweet(browser_dets['page'], "Hello, World!\nWelcome to my timeline!")
        #reply tweet
        '''
        browser_dets['page'].goto('https://twitter.com/stats_feed/status/1682085617872543754')
        time.sleep(3)
        post_tweet(browser_dets['page'], "Interesting!", button_name='Reply')
        '''

if __name__ == "__main__":
    main()
