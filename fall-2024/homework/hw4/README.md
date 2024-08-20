# Homework 4 - Exploring Social Networks
**Due:** October 31, 2024 by 11:59pm

Read through the entire assignment before starting. *Do not wait until the last minute to start working on it.* 

## Assignment

You will investigate the [friendship paradox](http://en.wikipedia.org/wiki/Friendship_paradox) on Facebook, which says "most people have fewer friends than their friends have, on average." 

**Reminder about Programming Tasks:** For several of the programming tasks this semester, you will be asked to write code to operate on 100s or 1000s of data elements.  If you have not done this type of development before, I *strongly encourage* you to start small and work your way up.  Especially when you are using new tools or APIs, start on a small test dataset to make sure you understand how to use the tool and that your processing scripts are working before ramping up to the full set. *This will save you an enormous amount of time.*

Write a report that contains the answers and *explains how you arrived at the answers* to the following questions. Before starting, review the [HW report guidelines](https://github.com/anwala/teaching-web-science/blob/main/fall-2023/homework/hw0/reports.md).  Name your report for this assignment `hw4_report` with the proper file extension.


(**Report (2 points**)

### Q1. Friendship Paradox on Facebook (8 points)

Determine if the friendship paradox holds for a user's Facebook account. *(This used to be more interesting when you could more easily download your friend's friends list from Facebook. Facebook now requires each friend to approve this operation, effectively making it impossible.)* 

acnwala_friends_friends_count.csv (provided on Piazza) contains a user's friends' names and number of friends they each have.

*Q: What is the mean, standard deviation, and median of the number of friends that the user's friends have?*  

Create a graph of the number of friends (y-axis) and the friends themselves (x-axis), sorted by number of friends. The friends don't need to be labeled
on the x-axis: 1, 2, 3,..., n should be sufficient. Include the user in the graph in the appropriate sorted position (count the number of their friends) and label as *U*.

*Q: Does the friendship paradox hold for this user and their friends on Facebook?*
<!--
### Q2. Friendship Paradox on Twitter (4 points)

Determine if the friendship paradox holds for your Twitter account. Since Twitter is a directed graph, use *followers* as the value you measure (i.e., "do your followers have more followers than you?").  

If you have less than 50 followers on Twitter, then you can do the analysis for another Twitter account (e.g., my account is [acnwala](https://twitter.com/acnwala/)) and substitute the user you pick for *you* in the questions below.

*Q: What is the mean, standard deviation, and median of the number of followers that your followers have?*  

*Q: Does the friendship paradox hold for you and your followers on Twitter?*

You may use Twarc2 in Python to access the Twitter API to find a user's followers.  The code to access the Twitter API should be similar to [get_tweets.py](https://github.com/anwala/teaching-web-science/blob/main/fall-2023/homework/hw0/get_tweets.py), you may use that to start.

Other helpful references:
* [Labs for the Standard Product Track in Python](https://github.com/twitterdev/getting-started-with-the-twitter-api-v2-for-academic-research/blob/main/modules/6b-labs-code-standard-python.md) - look at the section headings to find the appropriate part to read
* [Twitter's User object model](https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/user) - explains the data structure returned from the Twitter API
* [process-tweets.py](https://github.com/anwala/teaching-web-science/blob/main/fall-2023/homework/hw0/process_tweets.py) - shows examples of accessing different parts of the data structure returned from the Twitter API

## Extra Credit

### Q3. *(1 points)* 
Repeat Q2, but change *followers* to *following*.  

*Q: Are the people you are `following`, follow more people than you are?*

### Q4. *(1 points)*  
Twitter friendships can be uni-directional or bi-directional.

*Q: How many friendships do you have on Twitter?*  

List the usernames of those who have a bi-directional relationships with you. (If there are more than 20, put the list in a separate file in your repo and provide the filename in your report.)
-->
## Submission

Make sure that you have committed and pushed your local repo to your private GitHub repo (inside the `hw4` folder).  Your repo should include your report, images, code, and data you developed to answer the questions. Include "Ready to grade @anwala" in your final commit message. 
