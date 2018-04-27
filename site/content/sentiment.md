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
  <img src="/GaggleOfKaggle/img/r_sentiment_dist.png" width=200px>
  <img src="/GaggleOfKaggle/img/python_sentiment_dist.png" width=200px>
  <div class="caption">R Sentiment (Left) vs. Python Sentiment (Right)</div>
</div>

We found the two used slightly different approaches towards identifying sentiment, and as a result, the R library was able to tease out more information than the Textblob option, as shown above. As a result, we opted to work with the R based approach, since it gives us more diversity in the data to explore.

Sentiment By Day
--------------------------------

With daily stock prices in hand, we wanted to analyze the sentiment of each headline for a given day in order to potentially find a correlation between the two. We calculated the daily sentiment in three ways: Mode (the most common direction for headlines of a given day), Sum (the sum of all the sentiment scores for a given day), and Mean (the mean of the sentiment scores for a given day).

The distribution of sentiment for headlines based on the Mode had mostly Neutral days and very few positive days:
<div align=center>
  <img src="/GaggleOfKaggle/img/SentimentModeDist.png" width=200px>
  <div class="caption">Sentiment Distribution - Mode</div>
</div>

The distributions for sentiment based on the Sum and Mean were the same, and were overwhelmingly Negative:

<div align=center>
  <img src="/GaggleOfKaggle/img/SentimentSumDist.png" width=200px>
  <img src="/GaggleOfKaggle/img/SentimentMeanDist.png" width=200px>
  <div class="caption">Sentiment Distribution - Sum (Left) vs. Mean (Right)</div>
</div>

Looking at the sentiments by day using Sum and Mean provided a different picture. The sentiments fluctuate, but there are clearly some days that have more positive or negative headlines than others:

<div align=center>
  <img src="/GaggleOfKaggle/img/SentimentSumDay.png" width=200px>
  <div class="caption">Sentiment by Day - Sum</div>
</div>

<div align=center>
  <img src="/GaggleOfKaggle/img/SentimentMeanDay.png" width=200px>
  <div class="caption">Sentiment by Day - Mean</div>
</div>

Word Popularity
--------------------------------

With an understanding of the sentiment, we now wanted to see what was the most popular words used in headlines. To determine this we used the [WordCloud](https://github.com/amueller/word_cloud) library for Python to filter out stop words, then generate a wordmap with the most frequent terms relatively larger to lesser used ones. We then used the Python Imaging Library to stencil this cloud onto a map of Australia - in spirit of the project.

<div align=center>
  <img src="/GaggleOfKaggle/img/wordmap.png">
  <div class="caption">Popular terms include the US, Winning, Plan, New, and Say.</div>
</div>
