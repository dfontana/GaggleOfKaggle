+++
date = "2018-04-28"
draft = false
title = "Conclusion and Final Thoughts"
weight = 6
type = "post"
+++

> How does daily overall sentiment affect the value of an industry?

We started this project asking a very simple question - or so we thought. We wanted to know how the attitude towards a company could impact its stock's value. It turns out that question brings a lot more weight than we could have anticipated:

- Finding companies in headlines is *hard* - it's a working problem in NLP!
- Generalizing sentiment for a day helps us get around that, but it skews our evaluation of individual components (the headlines about a different company doesn't impact all others!)
- Many models aren't perfect, but there are some that might hold some promise.

Ideally from here we'd like to work more on the Named Entity Extraction process so we can truly connect a headline with a specific business. If we can't isolate that a headline is related to a specific company or industry, then there's not much sentiment can tell us other than how the general market may be doing. Working on optimizing the neural network model after that would be ideal - our presented models show some early promises that could be better tuned. [HyperOpt](https://github.com/hyperopt/hyperopt) is a great library to help automate the searching of models, but we might want to first revisit the type of Neural Network we used.

The bigger picture
--------------

There's lots of ways to gain insight on Stocks: [MACD](https://www.investopedia.com/terms/m/macd.asp), [Support and Resistance](https://www.investopedia.com/trading/support-and-resistance-basics/), [Relative Strength Index](https://www.investopedia.com/terms/r/rsi.asp)... amoung many others. For example, here's a basic regression predicting the stock value direction based on closing prices *30 days prior*.

<div align=center>
  <img src="/GaggleOfKaggle/img/close_regression.png" width=400>
  <div class="caption">A simple regression predicting closing prices based on a 30 day window (blue). Training data is in black while testing data is in yellow.</div>
</div>

The bigger takeaway is that no single indicator trumps them all. Combining different ones to gain a more well-rounded prediction is a more strategic approach to automated trading, which is why adding Sentiment Analysis can help bolster a prediction. One of the advantages of Sentiment is that it can capture more knee-jerk reactions a stock may take throughout a day. Imagine breaking news hits a company is in dire straights, or holding high potential for days on end - while other means may see that, it won't be until after people have already started trading on that news. Combining Sentiment could help get your trade in sooner than the rest.

The work done in this project, then, is a stepping stone in this direction.