+++
date = "2018-04-20"
draft = false
title = "Sentiment Analysis"
weight = 3
type = "post"
+++

Sentiment Distribution
--------------------------------

To better understand the mood of our headlines, we needed to look at the distribution of Sentiment expressed by them; whether they were `Positive`, `Neutral`, or `Negative`. To do this we attempted both an analysis in the Python [Textblob](http://textblob.readthedocs.io/en/dev/) library, which is built atop [NLTK](https://www.nltk.org/) and in the R [Sentiment Analysis](https://cran.r-project.org/web/packages/SentimentAnalysis/SentimentAnalysis.pdf) library.

<div align=center>
  <img src="/GaggleOfKaggle/img/python_sentiment_dist.png" width=200px>
  <img src="/GaggleOfKaggle/img/r_sentiment_dist.png" width=200px>
  <div class="caption">R Sentiment (Left) vs. Python Sentiment (Right)</div>
</div>

We found the two used slightly different approaches towards identifying sentiment, and as a result, the R library was able to tease out more information than the Textblob option, as shown above. As a result, we opted to work with the R based approach, since it gives us more diversity in the data to explore.

Word Popularity
--------------------------------

With an understanding of the sentiment, we now wanted to see what was the most popular words used in headlines. To determine this we used the [WordCloud](https://github.com/amueller/word_cloud) library for Python to filter out stop words, then generate a wordmap with the most frequent terms relatively larger to lesser used ones. We then used the Python Imaging Library to stencil this cloud onto a map of Australia - in spirit of the project.

<div align=center>
  <img src="/GaggleOfKaggle/img/wordmap.png">
  <div class="caption">Popular terms include the US, Winning, Plan, New, and Say.</div>
</div>