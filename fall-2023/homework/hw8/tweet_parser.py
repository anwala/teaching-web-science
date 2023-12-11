# tweet_parser.py
# MCW/ACN - 11/16/2021, 08/07/2023

from scrape_twitter import get_timeline_tweets
from NwalaTextUtils.textutils import genericErrorInfo

def parse(browser_dets, screen_name, num_tweets=50):
    
    '''
        screen_name: Twitter screen_name
        num_tweets: Number of tweets to request (default: 50)
        returns dict with {'screen_name': screen_name, 'tweets': [tweet text 1, tweet text 2, ...]}
    '''

    tweet_data = []
    try:
        tweets = get_timeline_tweets(browser_dets, screen_name, max_tweets=num_tweets)
        tweet_data = [t['text'] for t in tweets['tweets'] if 'text' in t]
    except:
        genericErrorInfo()
  
    account_data = {'screen_name': screen_name, 'tweets': tweet_data}
    return account_data
