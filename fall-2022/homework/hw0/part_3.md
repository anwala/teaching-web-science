# Twitter API, twarc (3 points)

The goal of this assignment is to introduce you to the [Twitter API](https://developer.twitter.com/en/docs/twitter-api) through a wrapper application called [twarc](https://twarc-project.readthedocs.io/en/latest/twarc2_en_us/).

Once you have performed the steps described in [Twitter Setup](twitter_setup.md), including receiving approval for Twitter Developer Access and installing `twarc2`, you can work on the steps below.

You may use `twarc2` as a command-line application (e.g., for testing), but for your homework assignments, you will be using twarc [programmatically as a Python library](https://twarc-project.readthedocs.io/en/latest/#use-as-a-library).

## General Notes
For assignments that require you to obtain data from the web and process it, you are encouraged to separate those two tasks.  Create one script that collects the data and another script that processes the data.  That way, if there's an error in your processing script, you don't have to collect the data again.

You are encouraged to look at the code in the provided scripts ([get_tweets.py](get_tweets.py) and [process_tweets.py](process_tweets.py)) to see how the extraction and processing was done, but for now the main point is to make sure that you can access tweets programmatically.

## Q1. Collecting Tweets (1.5 points)

Download [get_tweets.py](get_tweets.py) and edit the code to point to the file where twarc has stored your Twitter API keys.  

Use `get_tweets.py` to collect 25 recent English-language tweets with links for any topic that interests you (e.g., `covid`). To do this, run the following command.

`% python3 get_tweets.py "covid"`

The output will be saved in `tweets.jsonl`.
Add a screenshot of a snippet of the output `tweets.jsonl` to your report.

## Q2. Processing Tweets (1.5 points)

Download [process_tweets.py](process_tweets.py) and use it to save information about each of the collected tweets to a file:

`% python3 process_tweets.py < tweets.jsonl > tweets_info.txt`

For each tweet in the file, this script will print the tweet ID, creation time, author, Twitter-assigned entities, and links included in the tweet.

Add a screenshot of a snippet of the output to your report.