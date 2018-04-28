+++
date = "2018-04-20"
draft = false
title = "The Data"
weight = 2
type = "post"
+++

Our data initially included two, semi-related datasets from Kaggle. <img align="right" src="/GaggleOfKaggle/img/kaggle.png" width=200px> The first consists of all the headlines written by [The Australian Broadcasting Corp](http://www.abc.net.au/) between 2003 and 2017, comprising of 1,103,665 records. Each record tracks the date the headline was published (in `YYYY-MM-DD` format) and the text within the headline - all words fully lowercased. Later when we talk about stitching our datasets together you will learn we decided to scrap this data set and scrap our own from the ABC archives. The structure of that dataset is exactly the same, but it spans from 2006 instead of 2003 and (more importantly), it preserves the casing and grammar of the original headlines. *Spoiler alert:* it turns out Natural Language tools rely on word casing to predict named entities within sentences.

<div align=center>
  <img src="/GaggleOfKaggle/img/headline.png">
  <div class="caption">Example records from headline data</div>
</div>

Our second dataset consists of daily stock values for all companies on the [Australian Securities Exchange](https://www.asx.com.au/). 6,475,470 records span from 1997 to the end of 2017, each tracking: the company’s ticker, the date of trade (in `YYYY-MM-DD` format), the opening/close/high/low price of the stock (all four being numerics representing the stocks value for that date), and the numeric trading volume of the stock for that date.

<div align=center>
  <img src="/GaggleOfKaggle/img/ticker_value.png">
  <div class="caption">Example records from ticker value data</div>
</div>

In addition to stock data for each company, we have a list of tickers associated to their full company name, and that company’s industry (categorical). In total there are 2,227 unique companies with the aforementioned features. It is interesting to note there only 26 unique industries, so we may take competition within industry into account in future modeling.

<div align=center>
  <img src="/GaggleOfKaggle/img/ticker_industry.png">
  <div class="caption">Example records from ticker to company association data</div>
</div>