import gzip
import json

def proc_tweet(tweet_data):

    if( tweet_data['notes']['is_retweet'] is True ):
        print('Retweeted by:', tweet_data['notes']['timeline_screen_name'])

    # gather some information about the tweet
    screen_name = tweet_data['user']['screen_name']  # author's username
    created_at = tweet_data['created_at']      # time tweet created
    verified = tweet_data['user']['verified']  # author verified?
    text = tweet_data['text']  # text of the tweet
    uid = tweet_data['id_str']  # tweet id

    # collect links 
    links = []
    if 'urls' in tweet_data.get('entities', []):
        for link in tweet_data['entities']['urls']:
            links.append(link['expanded_url'])
    

    # print information about the tweet
    print (uid + "\t" + created_at + "\t" + screen_name)
    for link in links:
        print("  " + link)
    print ()    

with gzip.open('acnwala_timeline.json.gz', 'rb') as infile:
            
    counter = 1
    for tweet in infile:
        tweet = json.loads(tweet.decode())
        
        print(f'reading tweets: {counter}')
        proc_tweet(tweet)
        print()
        counter += 1
        
