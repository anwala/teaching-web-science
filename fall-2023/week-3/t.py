import requests
import time

from NwalaTextUtils.textutils import getLinks
from playwright.sync_api import sync_playwright

def is_logged_in(links):
    logged_in_links = ['https://twitter.com/home', 'https://t.co/']
    
    for l in links:
        for log_l in logged_in_links:
            if( l['link'].startswith(log_l) ):
                return True
    return False

def get_timeline_tweets(screen_name, max_pages=1):

    if( max_pages < 0 ):
        return []

    screen_name = screen_name.strip()
    if( screen_name == '' ):
        return []

    tweets = []
    dedup_set = set()
    


    logger.info('\nget_timeline_tweets():')
    for i in range(max_pages):

        user_id_det = '' if user_id == '' else f' (id: {user_id})'
        logger.info('\tpage: ' + str(i+1) + ' of ' + str(max_pages) + ', for: @' + screen_name + f'{user_id_det}')

        #guess max_id, since_id - start
        if( timeline_startdate != '' ):
            try:
                timeline_next_date = timeline_startdate + timedelta(hours=timeline_scroll_by_hours)
                next_twt_id = gen_post_snowflake_twitter_id(timeline_startdate)

                params.pop('max_id', None)
                params.pop('since_id', None)

                if( timeline_scroll_by_hours > 0 ):
                    params['since_id'] = next_twt_id
                else:
                    params['max_id'] = next_twt_id

                logger.info('\ttimeline_startdate: ' + str(timeline_startdate) + ' (' + str(timeline_scroll_by_hours) + ') -> ' + str(next_twt_id) )

            except:
                genericErrorInfo()
        #guess max_id, since_id - end


        try:
            response = oauth.get("https://api.twitter.com/1.1/statuses/user_timeline.json", params=params)
            timeline = json.loads(response.text)
        except:
            genericErrorInfo()
            

        if( 'errors' in timeline ):
            logger.error( '\terror: ' + str(timeline['errors']) )
            #to conform with 1 request per second rate limit for user auth: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/api-reference/get-statuses-user_timeline
            time.sleep(1)
            continue

        if( isinstance(timeline, dict) or len(timeline) == 0 ):
            #to conform with 1 request per second rate limit for user auth: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/api-reference/get-statuses-user_timeline
            time.sleep(1)
            continue
        
        
        #dedup tweets - start
        for twt in timeline:
            
            if( 'id' not in twt ):
                continue

            if( twt['id'] in dedup_set ):
                continue

            dedup_set.add( twt['id'] )
            tweets.append(twt)
        #dedup tweets - end
        logger.info( f'\t{len(tweets)} tweets' )


        if( timeline_startdate == '' ):
            #use default timeline pagination since user is not paginating by time
            params['max_id'] = timeline[-1]['id'] - 1
        else:
            timeline_startdate = timeline_next_date
            logger.info('\tpaginating with datetime: ' + str(timeline_startdate) + '\n' )


        sleep_flag = True
                    
        if( sleep_flag ):
            #to conform with 1 request per second rate limit for user auth: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/api-reference/get-statuses-user_timeline
            time.sleep(1)

    return tweets

def re_hydrate_tweet():

    #https://github.com/JustAnotherArchivist/snscrape/issues/996
    url = "https://cdn.syndication.twimg.com/tweet-result"
    querystring = {"id":"1652193613223436289","lang":"en"}

    payload = ""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Origin": "https://platform.twitter.com",
        "Connection": "keep-alive",
        "Referer": "https://platform.twitter.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "TE": "trailers"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    print(response.text)

def get_auth_twitter_pg(playwright):
    
    print('\nget_auth_twitter_pg()')

    chromium = playwright.firefox #"chromium" or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    
    sleep_seconds = 3
    page.goto('https://twitter.com/login')
    
    while( True ):

        print(f'\twaiting for login, sleeping for {sleep_seconds} seconds')
        
        time.sleep(sleep_seconds)
        page_html = page.content()
        page_links = getLinks(uri='', html=page_html, fromMainTextFlag=False)
        #print( page.url, 'links:', len(page_links) )

        if( is_logged_in(page_links) ):
            return {
                'page': page,
                'browser': browser
            }
    
    return {}

#'''
with sync_playwright() as playwright:
    payload = get_auth_twitter_pg(playwright)
    payload['page']
    payload['browser']

#'''

'''
from getpass import getpass
pwd = getpass('Password:')
print('pwd:', pwd)
'''