# Homework 5 - Graph Partitioning
**Due:** November 12, 2024 by 11:59pm
Read through the entire assignment before starting.  *Do not wait until the last minute to start working on it.* 

## Assignment

You will investigate the split of the Karate Club (Zachary, 1977), described starting on [slide 92 in the Module-07 Social Networks lecture slides](https://docs.google.com/presentation/d/1Bey47wfUnBEy4O6j-T2X7y_bT0YNM6CN/edit#slide=id.p92).  You must use a Python or JavaScript library (as discussed in [Module-09 Graph Vis](https://docs.google.com/presentation/d/1IUZzjgbVsKWcWKq24FfWM8rtZPQLFutS/edit#slide=id.p1)) to generate the graphs required in this assignment.

Write a report that answers and *explains how you arrived at the answers* to the following questions. Include any interesting findings that you discover from your analysis.

Write a report that contains the answers and *explains how you arrived at the answers* to the following questions. Before starting, review the [HW report guidelines](https://github.com/anwala/teaching-web-science/blob/main/fall-2022/homework/hw0/reports.md).  Name your report for this assignment `hw5_report` with the proper file extension.

(**Report (2 points**)

### Q1. Color nodes based on final split (2 points)

Draw the original Karate club graph (before the split) and color the nodes according to the factions they belong to (John A or Mr. Hi). This should look similar to the graph on slide 92 - all edges should be present, just indicate the nodes in the eventual split by color.

*Q: How many nodes (students) eventually go with John and how many with Mr. Hi?*
 
### Q2. Use the Girvan-Newman algorithm to illustrate the split (4 points)

We know the final result of the Karate Club split, which you've colored in Q1. Use the Girvan-Newman algorithm to check if the split could have been predicted by the social interactions expressed by edges. How well does the mathematical model represent reality?  Generously document your answer with all supporting equations, code, graphs, arguments, etc.

Keeping the node colors the same as they were in Q1, run multiple iterations of the Girvan-Newman graph partioning algorithm (see Module-07 Social Networks, slides 90-99) on the Karate Club graph until the graph splits into two connected components. Include an image of the graph after each iteration in your report.  

Note: Implement the Girvan-Newman algorithm (See Module-07, slide 91) rather than relying on a built-in function which hide the intermediate steps. Narrate in your report, the workings of the Girvan-Newman algorithm.

*Q: How many iterations did it take to split the graph?* 

### Q3. Compare the actual to the mathematical split (2 points)

Compare the connected components of the Girvan-Newman split graph (Q2) with the connected components of the actual split Karate club graph (Q1).

*Q: Did all of the same colored nodes end up in the same group?  If not, what is different?*


### Useful Resources

* Wayne Zachary, ["An Information Flow Model for Conflict and Fission in Small Groups"](http://aris.ss.uci.edu/~lin/76.pdf), 1977 - original paper 
* [Zachary's Karate Club](https://en.wikipedia.org/wiki/Zachary's_karate_club) (Wikipedia)
* Data 
   * matrix format: [UCINET IV Version 1.0 DATASETS](http://vlado.fmf.uni-lj.si/pub/networks/data/Ucinet/UciData.htm#zachary)
   * GML file: [Gephi Datasets](https://github.com/gephi/gephi/wiki/Datasets)
   * [karate_club_graph()](https://networkx.org/documentation/stable/auto_examples/graph/plot_karate_club.html) in [NetworkX](https://networkx.org/documentation/stable/index.html)
* Example code
  * [DATA 440-03 Google Colab notebook](https://github.com/anwala/teaching-web-science/blob/main/fall-2022/week-9/data_440_03_f22_mod_09_networkx_example.ipynb)
  * [CommunityGirvanNewman](https://snap.stanford.edu/snappy/doc/reference/CommunityGirvanNewman.html) in [Snap.py](https://snap.stanford.edu/snappy/doc/tutorial/index-tut.html) 
  * [community_edge_betweenness()](https://igraph.org/python/doc/api/igraph.Graph.html#community_edge_betweenness) in [igraph-python](https://igraph.org/python/) 
  * [edge_betweenness_centrality()](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.edge_betweenness_centrality.html#networkx.algorithms.centrality.edge_betweenness_centrality) in [NetworkX](https://networkx.org/)
  * [number_connected_components()](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.components.number_connected_components.html#networkx.algorithms.components.number_connected_components) in [NetworkX](https://networkx.org/)
  * ["What are the differences between community detection algorithms in igraph?"](http://stackoverflow.com/questions/9471906/what-are-the-differences-between-community-detection-algorithms-in-igraph/9478989#9478989), StackOverflow question/answer
  * ["Are there implementations of algorithms for community detection in graphs? "](http://stackoverflow.com/questions/5822265/are-there-implementations-of-algorithms-for-community-detection-in-graphs), StackOverflow question/answer


## Extra Credit
<!--
### Q4. *(2 points)*
We know the group split into two different groups.  Suppose the disagreements in the group were more nuanced.  What would the clubs look like if they split into 3, 4, and 5 groups?  A single node can be considered as a "group".

### Q4. *(2 or 4 or 6 points)*
Use D3.js's force-directed graph layout to draw the Karate Club Graph before the split. Color the nodes according to the factions they belong to (John A or Mr. Hi). After a button is clicked, split the graph based on the original graph split. Include a link to the HTML/JavaScript files (or Observable notebook) in your report and all necessary screenshots.
* If you load a new file containing the split upon button press, this EC is worth 2 points.
* If you modify the nodes and edges using D3 (without loading a new file), this EC is worth 4 points.
* If you use D3 transitions to move the nodes and edges to their new locations, this EC is worth 6 points.
-->
### Q4. *(2 points)*
Use D3.js's force-directed graph layout to draw the Karate Club Graph before the split. Color the nodes according to the factions they belong to (John A or Mr. Hi). After a button is clicked, split the graph based on the original graph split. Include a link to the HTML/JavaScript files (or Observable notebook) in your report and all necessary screenshots.
* If you load a new file containing the split upon button press, this EC is worth 2 points.

## Submission

Make sure that you have committed and pushed your local repo to your private GitHub repo (inside the `hw5` folder).  Your repo should include your report, images, code, and data you developed to answer the questions. Include "Ready to grade @anwala" in your final commit message. 