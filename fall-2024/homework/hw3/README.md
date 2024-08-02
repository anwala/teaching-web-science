# Homework 3 - Ranking Webpages
**Due:** October 17, 2024 by 11:59pm
Read through the entire assignment before starting.  *Do not wait until the last minute to start working on it.* 

## Assignment

You will investigate different ways to rank webpages based on a query.  Write a report that answers and *explains how you arrived at the answers*. Include any interesting findings that you discover from your analysis.
 
**Note about Programming Tasks:** For several of the programming tasks this semester, you will be asked to write code to operate on 100s or 1000s of data elements.  If you have not done this type of development before, I *strongly encourage* you to start small and work your way up.  Especially when you are using new tools or APIs, start on a small test dataset to make sure you understand how to use the tool and that your processing scripts are working before ramping up to the full set. *This will save you an enormous amount of time.*

Write a report that contains the answers and *explains how you arrived at the answers* to the following questions. Before starting, review the [HW report guidelines](https://github.com/anwala/teaching-web-science/blob/main/fall-2023/homework/hw0/reports.md).  Name your report for this assignment `hw3_report` with the proper file extension.


(**Report (2 points**)

### Q1. Data Collection (4 points)

*For the following tasks, consider which items could be scripted with a shell script or Python. Consider creating separate scripts for different tasks. Determine the best way to collect the data.*

Download the HTML content of the 1000 unique URIs you gathered in HW2 and strip out HTML tags (called "boilerplate") so that you are left with the main text content of each webpage.  ***Plan ahead because this will take time to complete.***

Note: If you plan completing this question in Windows PowerShell (instead of Linux), you will need to be aware of how PowerShell [uses character encoding for string data](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding?view=powershell-7.1) (see also [Understanding file encoding in VS Code and PowerShell](https://docs.microsoft.com/en-us/powershell/scripting/dev-cross-plat/vscode/understanding-file-encoding?view=powershell-7.1)).

#### Saving the HTML Files

`curl`, `wget`, or `lynx` are all good candidate programs to use.  We want just the raw HTML, not the images, stylesheets, etc.

Save the HTML content returned from each URI in a uniquely-named file.  The easiest thing is to use the URI itself as the filename, but your shell will likely not like some of the characters that may occur in URIs (e.g., "?", "&").  My suggestion is to hash the URIs to associate them with their respective filename using a [cryptographic hash function](https://en.wikipedia.org/wiki/Cryptographic_hash_function), like MD5.  

For example, https://www.cnn.com/world/live-news/nasa-mars-rover-landing-02-18-21 hashes to `2fc5f9f05c7a69c6d658eb680c7fa6ee`:
```console
$ echo -n "https://www.cnn.com/world/live-news/nasa-mars-rover-landing-02-18-21" | md5sum | awk '{print $1}'
2fc5f9f05c7a69c6d658eb680c7fa6ee
```
Notes:
* `md5sum` might be `md5` on some machines
* note the `-n` option to `echo` -- this removes the trailing newline
* `awk '{print $1}'` prints only the characters before the first space in the output (i.e., the hash) -- *try the command without this to see the difference*

Here are some ways you could download the HTML from that URI using the hash as the filename:
* `$ curl "https://www.cnn.com/world/live-news/nasa-mars-rover-landing-02-18-21" > 2fc5f9f05c7a69c6d658eb680c7fa6ee.html`
* `$ wget -O 2fc5f9f05c7a69c6d658eb680c7fa6ee.html https://www.cnn.com/world/live-news/nasa-mars-rover-landing-02-18-21`
* `$ lynx -source https://www.cnn.com/world/live-news/nasa-mars-rover-landing-02-18-21 > 2fc5f9f05c7a69c6d658eb680c7fa6ee.html`

For later analysis, you will need to map the content back to the original URI, so create a text file that contains all of the URI to hash mappings.

#### Removing HTML Boilerplate

Now use a tool to remove (most) of the HTML markup from your 1000 HTML documents. 

The Python boilerpy3 library will do a fair job at this task.  You can use `pip` to install this Python package.  The [main boilerpy3 webpage](https://pypi.org/project/boilerpy3/) has several examples of its usage.

Keep both files for each URI (i.e., raw HTML and processed), and upload both sets of files to your GitHub repo. Put the raw and processed files in separate folders.  Remember that to upload/commit a large number of files to GitHub, [use the command line](https://docs.github.com/en/github/managing-files-in-a-repository/adding-a-file-to-a-repository-using-the-command-line).

Sometimes boilerpy3 is unable to extract the downloaded HTML (either it's all boilerplate or it's not actually HTML), so it produces no output, resulting in a 0B size file.  You may also run into HTML files that trigger UnicodeDecode exceptions when using boilerpy3.  You can skip files that have these types of encoding errors, result in 0B output, or contain inappropriate content (whatever you define as such). The main goal is to have enough processed files so that you can find 10 documents that contain your query term (for Q2 and later).

*Q: How many of your 1000 URIs produced useful text? If that number was less than 1000, did that surprise you?* 
 
### Q2. Rank with TF-IDF (4 points)

Choose a query term (e.g., "coronavirus") that is not a stop word (e.g., "the"), or super-general (e.g., "web"), or in HTML markup (e.g., "http") that is found in at least 10 of your documents.  If the term is present in more than 10 documents, choose any 10 English-language documents from *different domains* from the result set. 

Hint: You may want to use the Unix command `grep -c` on the processed files to help identify a good query -- it indicates the number of lines where the query appears:
```console
% cat 2fc5f9f05c7a69c6d658eb680c7fa6ee.html | grep -c coronavirus
```

As per the example in the [Module 06 slides](https://docs.google.com/presentation/d/1YFvaT8n-t5G8npk5c3kj31DN4kddMy-W/edit?usp=sharing), compute TF-IDF values for the query term in each of the 10 documents and create a table with the TF, IDF, and TF-IDF values, as well as the corresponding URIs. (If you are using LaTeX, you should create a [LaTeX table](https://www.overleaf.com/learn/latex/tables).  If you are using Markdown, view the raw version of this file to see how to generate a table.) Rank the URIs in decreasing order by TF-IDF values.  For example:

Table 1. 10 Hits for the term "shadow", ranked by TF-IDF.

|TF-IDF |TF |IDF  |URI
|------:|--:|---:|---
|0.150  |0.014  |10.680 |http://foo.com/
|0.044  |0.008  |10.680 |http://bar.com/

You can use Google or Bing for the DF estimation.  If you use Google, use 35 billion as the total size of the corpus, and if you use Bing, use 8 billion as the total size of the corpus (based on data from https://www.worldwidewebsize.com).

To count the number of words in the processed document (i.e., the denominator for TF), you can use the Unix command `wc`:

```console
% wc -w 2fc5f9f05c7a69c6d658eb680c7fa6ee.processed
    19261 2fc5f9f05c7a69c6d658eb680c7fa6ee.processed
```
It won't be completely accurate, but it will be probably be consistently inaccurate across all files.  You can use more 
accurate methods if you prefer, just explain your method.  

Don't forget the log base 2 for IDF, and mind your [significant digits](https://en.wikipedia.org/wiki/Significant_figures#Rounding_and_decimal_places).

*You must discuss in your report how you computed the values (especially IDF) and provide the formulas you used for TF, IDF, and TF-IDF.*  
<!--
## Extra Credit

### Q3. *(2 points)* 
Compute the [Kendall Tau_b score](https://en.wikipedia.org/wiki/Kendall_rank_correlation_coefficient#Tau-b) for the lists from Q2 (use "b" because there will likely be tie values in the rankings). Report both the Tau value and the "p" value.

### Q4. *(3 points)*  
Build a simple (i.e., no positional information) inverted file (in ASCII) for all the words from your 1000 URIs.  Upload the entire file to your GitHub repo and discuss an interesting portion of the file in your report.
-->
## Submission

Make sure that you have committed and pushed your local repo to your private GitHub repo (inside the `hw3` folder).  Your repo should include your report, images, code, and data you developed to answer the questions.  Include "Ready to grade @anwala" in your final commit message. 