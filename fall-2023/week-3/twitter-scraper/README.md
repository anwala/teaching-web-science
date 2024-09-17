## Twitter Scraper
Twitter has placed a [paywall](https://twitter.com/acnwala/status/1641231749928583170) over their once accessible API. This move has been widely [condemned by the research community](https://independenttechresearch.org/letter-twitters-new-api-plans-will-devastate-public-interest-research/) which is still grappling on [a way forward](https://docs.google.com/document/d/e/2PACX-1vQYX6jTdcoEi9Laq-PGVfv34g4vZvyF77JoKlMDcJNr15ixSbCcYkHaNdCOVUl7A06_Qn_vZJmc27Kd/pub). Multiple Web Science assignments (e.g., `HW2`, `HW6`, and `HW8`) were affected by this restriction. 

The following is a description of a simple (naive) application for [scraping](https://docs.google.com/presentation/d/1vtT9dleNJlUbc3ny14gotGX1Md1dEWhVHYWTz0MMdRk/edit?usp=sharing) tweets from with the Twitter website. I recommend creating a separate Twitter account before utilizing this application just in case the account is suspended.

## Installation
```bash
$ pip install -r requirements.txt
$ playwright install
```

## Usage/Examples

There are three primary ways to use this application as outlined by the following examples

### Example 1: Extract tweets from timeline

The following code block first loads `twitter.com` in the browser and waits for the user to login. Once the user is authenticated, it extracts a maximum of 20 tweets (`max_tweet = 20`) from the timeline of `@acnwala` using the `get_timeline_tweets()` function. Next it writes the retrieved tweets into a compressed `jsonl` file (`acnwala_timeline.json.gz`) using `write_tweets_to_jsonl_file().` Note that once the user is authenticated, the browser state is stored in `playwright-browser-storage` (change by setting `get_auth_twitter_pg()`'s `browser_storage_path` parameter), so no login would NOT be required subsequently.

```Python
from playwright.sync_api import sync_playwright
from scrape_twitter import get_auth_twitter_pg
from scrape_twitter import get_timeline_tweets
from util import write_tweets_to_jsonl_file

def main():

    with sync_playwright() as playwright:
        
        browser_dets = get_auth_twitter_pg(playwright)
        if( len(browser_dets) != 0 ):
        
            tweets = get_timeline_tweets(browser_dets, 'acnwala', max_tweets=20)
            write_tweets_to_jsonl_file('acnwala_timeline.json.gz', tweets['tweets'])

    #OR without with statement
    '''
    playwright = sync_playwright().start()
    browser_dets = get_auth_twitter_pg(playwright)
    
    if( len(browser_dets) != 0 ):
        tweets = get_timeline_tweets(browser_dets, 'acnwala', max_tweets=3)
        write_tweets_to_jsonl_file('acnwala_timeline.json.gz', tweets['tweets'])

    playwright.stop()
    '''

if __name__ == "__main__":
    main()
```

The content of the `acnwala_timeline.json.gz` may be read line by line with the following,
```Python
import gzip
import json

with gzip.open('acnwala_timeline.json.gz', 'rb') as infile:
            
    counter = 1
    for tweet in infile:
        tweet = json.loads(tweet.decode())
        
        print(f'reading tweets: {counter}')
        counter += 1
```

### Example 2: Extract tweets from search

The following code block accomplished the same task as Example 1, except, it extracts tweets from Twitter search results when supplied a given query (e.g., `william & mary`).

```Python
from playwright.sync_api import sync_playwright
from scrape_twitter import get_auth_twitter_pg
from scrape_twitter import get_search_tweets
from util import write_tweets_to_jsonl_file

def main():
    
    playwright = sync_playwright().start()
    browser_dets = get_auth_twitter_pg(playwright)

    if( len(browser_dets) != 0 ):
    
        tweets = get_search_tweets(browser_dets, 'william & mary', max_tweets=10)        
        write_tweets_to_jsonl_file('twitter_serp.json.gz', tweets['tweets'])

    playwright.stop()

if __name__ == "__main__":
    main()
```
Consider using the following to search for tweets containing links from `cnn.com` domain published between 2006-01-01 to 2006-12-31
```python
tweets = get_search_tweets(browser_dets, '"cnn.com" until:2006-12-31 since:2006-01-01', max_tweets=10)
```

### Example 3: Post a tweet or reply to tweet

The following code block posts the tweet `Hello, World!\nWelcome to my timeline!` on the authenticated user's timeline. The `post_tweet()` function does a simple post (or reply) without checking if the content is within Twitter's character limit.

```Python
from datetime import datetime
from playwright.sync_api import sync_playwright
from scrape_twitter import get_auth_twitter_pg
from scrape_twitter import post_tweet

with sync_playwright() as playwright:
        
    browser_dets = get_auth_twitter_pg(playwright)
    if( len(browser_dets) != 0 ):
        #True or False, post_tweet() should return the link of the newly posted tweet. 
        get_new_tweet_link = True

        #Twitter handle of account where message is to be posted
        twitter_account = 'lildarlin0'

        #reply_to_link should contain the link (e.g., 'https://twitter.com/xnwala/status/1699844461545836833') to the tweet to be replied to. Leave blank for isolated post
        reply_to_link = ''
         
        msg = f"\nHello again folks!\nWelcome to my timeline! Posting @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        post_status = post_tweet(browser_dets, msg, twitter_account=twitter_account, get_new_tweet_link=get_new_tweet_link, reply_to_link=reply_to_link)

        print('post_status:', post_status)
```
