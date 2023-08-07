## Twitter Scraper
Twitter has placed a [paywall](https://twitter.com/acnwala/status/1641231749928583170) over their once accessible API. This move has been widely [condemned by the research community](https://independenttechresearch.org/letter-twitters-new-api-plans-will-devastate-public-interest-research/) which is still grappling on [a way forward](https://docs.google.com/document/d/e/2PACX-1vQYX6jTdcoEi9Laq-PGVfv34g4vZvyF77JoKlMDcJNr15ixSbCcYkHaNdCOVUl7A06_Qn_vZJmc27Kd/pub). Multiple Web Science assignments (e.g., `HW2`, `HW6`, and `HW8`) were affected by this restriction. 

The following is a description of a simple (naive) application for [scraping](https://docs.google.com/presentation/d/1vtT9dleNJlUbc3ny14gotGX1Md1dEWhVHYWTz0MMdRk/edit?usp=sharing) tweets from with the Twitter website. I recommend creating a separate Twitter account before utilizing this application just in case the account is suspended.

## Installation
```bash
$ pip install -r requirements
$ playwright install
```

## Usage/Examples

There are three primary ways to use this application as outlined by the following examples

### Example 1: Extract tweets from timeline

The following code block first loads `twitter.com` in the browser and waits for the user to login. Once the user is authenticated, it extracts a maximum of 20 tweets (`max_tweet = 20`) from the timeline of `@acnwala` using the `get_timeline_tweets()` function. Next it writes the retrieved tweets into a compressed `jsonl` file (`acnwala_timeline.json.gz`) using `write_tweets_to_jsonl_file().`

```Python
from playwright.sync_api import sync_playwright
from scrape_twitter import get_auth_twitter_pg
from scrape_twitter import get_timeline_tweets
from util import write_tweets_to_jsonl_file

with sync_playwright() as playwright:
        
    browser_dets = get_auth_twitter_pg(playwright)
    if( len(browser_dets) != 0 ):
    
        tweets = get_timeline_tweets(browser_dets, 'acnwala', max_tweets=20)
        write_tweets_to_jsonl_file('acnwala_timeline.json.gz', tweets['tweets'])
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

with sync_playwright() as playwright:
        
    browser_dets = get_auth_twitter_pg(playwright)
    if( len(browser_dets) != 0 ):
    
        tweets = get_search_tweets(browser_dets, 'william & mary', max_tweets=20)        
        write_tweets_to_jsonl_file('twitter_serp.json.gz', tweets['tweets'])
```

### Example 3: Post a tweet

The following code block posts the tweet `Hello, World!\nWelcome to my timeline!` on the authenticated user's timeline. The `post_tweet()` function does a simple post without checking if the content is within Twitter's character limit.

```Python
from playwright.sync_api import sync_playwright
from scrape_twitter import get_auth_twitter_pg
from scrape_twitter import post_tweet

with sync_playwright() as playwright:
        
    browser_dets = get_auth_twitter_pg(playwright)
    if( len(browser_dets) != 0 ):
        post_tweet(browser_dets['page'], "Hello, World!\nWelcome to my timeline!")
```

### Example 4: Reply to a tweet

The following code block posts the tweet `Hello, World!\nWelcome to my timeline!` on the authenticated user's timeline. The `post_tweet()` function does a simple post without checking if the content is within Twitter's character limit.

```Python
import time
from playwright.sync_api import sync_playwright
from scrape_twitter import get_auth_twitter_pg
from scrape_twitter import post_tweet

with sync_playwright() as playwright:
        
    browser_dets = get_auth_twitter_pg(playwright)
    if( len(browser_dets) != 0 ):
        
        browser_dets['page'].goto('https://twitter.com/stats_feed/status/1682085617872543754')
        #Allow page to render so sleep. In the future consider using playwright's automated wait rather than time.sleep
        time.sleep(3)
        post_tweet(browser_dets['page'], "Very interesting!", button_name='Reply')
```