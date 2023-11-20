import os
import sys
import time

from getpass import getpass

from bs4 import BeautifulSoup
from datetime import datetime
from NwalaTextUtils.textutils import genericErrorInfo
from NwalaTextUtils.textutils import getLinks

from playwright.sync_api import sync_playwright
from urllib.parse import quote_plus

from util import paral_rehydrate_tweets
from util import readTextFromFile
from util import rehydrate_tweet
from util import write_tweets_to_jsonl_file
from util import writeTextToFile

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

def post_tweet(page, msg, button_name='Post', after_post_sleep=2.5):
    #Post, Reply
    # [id$='someId'] will match all ids ending with someId: https://stackoverflow.com/a/8714421
    eval_str = f''' document.querySelectorAll('[aria-label$="{button_name}"]')[0].click(); '''
    page.evaluate(eval_str)
    time.sleep(1)
    page.keyboard.type(msg, delay=20)
    page.evaluate(''' document.querySelectorAll('[data-testid="tweetButton"]')[0].click(); ''')

    #added because I observed that tweets were not posted without it
    time.sleep(after_post_sleep)

    
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

    prev_len = 0
    empty_result_count = 0
    
    tweet_links = set()
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
            tweet_links.add( tweet_link )
            twt_id = tweet_link.split('/status/')[-1]
            tweet_obj = rehydrate_tweet(twt_id)
            if( len(tweet_obj) == 0 ):
                print('\tOOPS! rehydration failed! patch rehydrate_tweet()')
                continue

            print( '\ttweets {}, datetime: {}, is_retweet: {}'.format(len(tweet_links), tweet_datetime, is_retweet) )
            print( f'\tdo stuff here with tweet_obj: {tweet_obj.keys()}\n' )
            #call your functions here to do stuff with tweet_obj like writing links to text file






            
            if( len(tweet_links) == max_tweets ):
                print(f'exiting reached ({len(tweet_links)}) maximum: {max_tweets}')
                sys.exit(0)

        empty_result_count = empty_result_count + 1 if prev_len == len(tweet_links) else 0
        if( empty_result_count > 5 ):
            print(f'No new tweets found, so exiting')
            sys.exit(0)

        prev_len = len(tweet_links)
        print('\tthrottling/scrolling, then sleeping for 2 second\n')
        scroll_down(page)
        time.sleep(2)
    

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

def stream_tweets(browser_dets, query, max_tweets=20):

    query = query.strip()
    if( max_tweets < 0  or len(browser_dets) == 0 or query == '' ):
        return {}

    print('\nstream_tweets():')
    uri = 'https://twitter.com/search?q=' + quote_plus(query) + '&f=live&src=typd'
    
    payload = {'self': uri, 'tweets': []}
    browser_dets['page'].goto(uri)
    
    get_tweet_ids_user_timeline_page( '', browser_dets['page'], max_tweets )

def try_to_login(page, username, password):

    print('\ntry_to_login()')
    username = username.strip()
    password = password.strip()

    if( username == '' or password == '' ):
        return
        
    page.get_by_role('textbox').fill(username)
    page.keyboard.press('Enter')
    page.get_by_label('Password', exact=True).type(password, delay=20)
    page.keyboard.press('Enter')

    
def get_auth_twitter_pg(playwright, callback_uri='', do_unsafe_login=True):
    
    print('\nget_auth_twitter_pg()')
    username = ''
    password = ''

    if( do_unsafe_login is True ):
        print('\t--- Unsafe login ---')

        if( os.path.exists('/tmp/unsafe_twitter_username.txt') and os.path.exists('/tmp/unsafe_twitter_password.txt') ):
            username = readTextFromFile('/tmp/unsafe_twitter_username.txt').strip()
            password = readTextFromFile('/tmp/unsafe_twitter_password.txt').strip()

        if( username == '' or password == '' ):
            username = input('\n\tEnter Twitter username: ')
            password = getpass('\tEnter Twitter password: ')

            writeTextToFile('/tmp/unsafe_twitter_username.txt', username)
            writeTextToFile('/tmp/unsafe_twitter_password.txt', password)

    chromium = playwright.firefox #"chromium" or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    sleep_seconds = 3
    page.goto('https://twitter.com/login')

    if( do_unsafe_login is True ):
        time.sleep(sleep_seconds)
        try_to_login(page, username, password)
    
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
                print(f'\tauthenticated, loaded {callback_uri}')
                
            print('\tsleeping for 3 seconds')
            time.sleep(3)
            return {
                'page': page,
                'context': context,
                'browser': browser
            }
    
    return {}

def main():
    
    if( len(sys.argv) != 3 ):
        print(f'Usage example:\n\tpython {sys.argv[0]} "williamsburg" 20')
        return
   
    with sync_playwright() as playwright:
        
        browser_dets = get_auth_twitter_pg(playwright)
        if( len(browser_dets) == 0 ):
            return
        
        stream_tweets(browser_dets, sys.argv[1], max_tweets=int(sys.argv[2]))

if __name__ == "__main__":
    main()