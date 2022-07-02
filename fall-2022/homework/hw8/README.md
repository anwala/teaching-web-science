# Homework 8 - Clustering
**Due:** Thursday, December 8, 2022 by 11:59pm
Read through the entire assignment before starting.  *Do not wait until the last minute to start working on it.* 

## Assignment

The goal of this assignment is to cluster Twitter accounts based on the content of their last 200 tweets.
 
**Important:** Much of the code for this assignment is provided for you, therefore, your report must include a high-level description of how the code works and answers to all of the sub-questions asked.

**Tips for Completing this Assignment:**
* Your first reference should be the [Module 12 lecture slides](https://docs.google.com/presentation/d/1QK7Of4o0gzYl2e0fSCOXuHlVMNflIUVJ/edit?usp=sharing), class [Colab notebook](), and *Programming Collective Intelligence* book and [Chapter 3 code](https://github.com/arthur-e/Programming-Collective-Intelligence/tree/master/chapter3).  *Don't start with a Google search.*

Write a report that contains the answers and *explains how you arrived at the answers* to the following questions. Before starting, review the [HW report guidelines](https://github.com/anwala/teaching-web-science/blob/main/fall-2022/homework/hw0/reports.md).  Name your report for this assignment `hw8_report` with the proper file extension.

(**Report (2 points**)

### Dataset
The MovieLens datasets were collected by the [GroupLens Research Project](https://grouplens.org/) at the University of Minnesota during the seven-month period from September 19, 1997 through April 22, 1998.  We are using the "100k dataset", available from
https://grouplens.org/datasets/movielens/100k/

There are three files that we will use:

1.  `u.data`: 100,000 ratings by 943 users on 1682 movies. Each user has rated at least 20 movies. Users and items are numbered
consecutively from 1. The data is randomly ordered. This is a tab-separated list of 

```
user id   item id   rating    timestamp
```

The timestamps are Unix seconds since 1/1/1970 UTC.

Example:
```
196     242     3       881250949
186     302     3       891717742
22      377     1       878887116
244     51      2       880606923
166     346     1       886397596
298     474     4       884182806
115     265     2       881171488
```

2.  `u.item`: Information about the 1682 movies. This is a tab-separated list of

```
movie id | movie title | release date | video release date | IMDb URL | unknown | Action | Adventure | Animation | Children's | Comedy | Crime | Documentary | Drama | Fantasy | Film-Noir | Horror | Musical | Mystery | Romance | Sci-Fi | Thriller | War | Western |
```

The last 19 fields are the genres. A 1 indicates the movie is of that genre, a 0 indicates it is not; movies can be in several genres at once. The movie ids are the ones used in the u.data dataset. 

Example:

```
161|Top Gun (1986)|01-Jan-1986||http://us.imdb.com/M/title-exact?Top%20Gun%20(1986)|0|1|0|0|0|0|0|0|0|0|0|0|0|0|1|0|0|0|0 
162|On Golden Pond (1981)|01-Jan-1981||http://us.imdb.com/M/title-exact?On%20Golden%20Pond%20(1981)|0|0|0|0|0|0|0|0|1|0|0|0|0|0|0|0|0|0|0 
163|Return of the Pink Panther, The (1974)|01-Jan-1974||http://us.imdb.com/M/title-exact?Return%20of%20the%20Pink%20Panther,%20The%20(1974)|0|0|0|0|0|1|0|0|0|0|0|0|0|0|0|0|0|0|0
``` 

Top Gun (1986) is genre "Action" and "Romance", On Golden Pond is genre "Drama", and Return of the Pink Panther is genre "Comedy".

3.  `u.user`: Demographic information about the users. This is a tab-separated list of:

```
user id | age | gender | occupation | zip code
```

The user ids are the ones used in the u.data dataset.

Example:
```
1|24|M|technician|85711 
2|53|F|other|94043 
3|23|M|writer|32067 
4|24|M|technician|43537 
5|33|F|other|15213
```

### Example Code
Instead of writing code from scratch (or searching for a solution online), modify the code from Ch 2 of *Programming Collective Intelligence* that performs movie recommendations.  If you make any modifications to the given code, be sure to note it in comments and in your report. There is code that we did not cover (contained in `recommendations.py`) that reads in the `u.data` and `u.item` files. 

Main source: https://github.com/arthur-e/Programming-Collective-Intelligence/blob/master/chapter2/recommendations.py  *(This code is written in Python 2, so if you use it directly, there may be changes required, as the `print` function in Python 3 requires parentheses.)*

[Class notebook w/examples](https://github.com/anwala/teaching-web-science/blob/main/fall-2022/week-11/data_440_03_f22_mod_11_pci_ch_02.ipynb)

Notes:
* You do not have to write a single Python script that answers all of the questions (*think modular!*). 
* You do not have write Python code for every operation. If you can answer questions using Unix commands or by manually scanning the data files, do so, but include the commands and describe what you did.
* You could pull the example code (that doesn't need modification) into a separate `.py` file and then use `import` in your script to use the needed functions.

Before starting, make sure that you understand what the functions `topMatches()` and `getRecommendations()` in the example code do.

## Questions

### Q1 (2 points)
Find 3 users who are closest to you in terms of age, gender, and occupation.  

For each of those 3 users:
* *A: What are their top 3 (favorite) films?*
* *B: What are their bottom 3 (least favorite) films?*

Based on the movie values in those 6 tables (3 users X (favorite + least favorite)), choose a user that you feel is most like you.  Feel free to note any outliers (e.g., "I mostly identify with user 123, except I did not like "Ghost" at all").  You can investigate more than just the top 3 and bottom 3 movies to find your best match.

This user is the *substitute you*.  

### Q2 (2 points)

Based on the ratings that users have given to the movies, answer the following questions:

* *A: Which 5 users are most correlated to the* substitute you *(i.e., which 5 users rate movies most similarly to the* substitute you?)
* *B: Which 5 users are least correlated (i.e., negative correlation)?*

### Q3 (2 points)
Compute ratings for all the films that the *substitute you* has not seen.  

Provide a list of the top 5 recommendations for films that the *substitute you* should see.  

Provide a list of the bottom 5 recommendations (i.e., films the *substitute you* is almost certain to hate).

### Q4 (2 points)
Choose your (the real you, not the *substitute you*) favorite and least favorite film from the data.  
For each film, generate a list of the top 5 most correlated and bottom 5 least correlated films. 

*Q: Based on your knowledge of the resulting films, do you agree with the results?*  In other words, do you personally like/dislike the resulting films?  
* If you have not heard of the recommended movies, search for the movie's trailer on YouTube and watch it before you answer.  If you do this, include the link to the trailer in your report.  For example, the [trailer for "Top Gun (1986)"](https://www.youtube.com/watch?v=xa_z57UatDY) was found by searching for "top gun 1986 trailer" on Google.   

## Extra Credit

### Q5 *(2 points)*

Filter the MovieLens dataset so that it only contains movies with at least 10 ratings.  

*A: How many movies are in the filtered dataset?*

Re-do Q3 and Q4 using this dataset.  

*B: Do you think the recommendations have improved?*

### Q6 *(2 points)*  

Rank all 1682 movies in the 1997/1998 MovieLens dataset.  (*Rank*, not rate. These should be 1-1682.) Break any ties based on number of raters (for example, a movie with an average rating of 4 with 100 raters should be ranked higher than a movie with an average rating of 4 with only 50 raters).

Place a file with the full list in your repo. List the top 10 and bottom 10 movies in your report.

### Q7 *(3 points)*  

Rank the 1682 movies in the 1997/1998 MovieLens dataset according to [today's IMDB data](https://www.imdb.com/interfaces/).  Note that the IMDB data includes TV shows and other items that aren't movies. Break any ties based on number of raters (for example, a movie with an average rating of 7.2 with 10,000 raters should be ranked higher than a movie with a rating of 7.2 with only 9,000 raters).

Place a file with the full list in your repo.  List the top 10 and bottom 10 movies in your report.

### Q8 *(3 point)*

*You must have done both Q6 and Q7 to complete this question.*

Draw a scatterplot where each dot is a film (i.e., 1682 dots).  The x-axis is the MovieLens ranking (Q6) and the y-axis is today's IMDB ranking (Q7).  Note that the MovieLens ratings are 1-5 and the IMDB ratings are 1-10, so you may want to normalize the data before plotting.  *The scatterplot must be created in R or Python, no Excel.*

*A: Describe any interesting outliers.*

## Submission

Make sure that you have committed and pushed your local repo to your private GitHub repo (inside the `hw8` folder).  Your repo should include your report, images, code, and data you developed to answer the questions. Include "Ready to grade @anwala" in your final commit message. 