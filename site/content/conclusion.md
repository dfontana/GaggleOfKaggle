+++
date = "2018-04-28"
draft = false
title = "Conclusion and Final Thoughts"
weight = 6
type = "post"
+++

> How does daily overall sentiment affect the value of an industry?

We started this project asking a very simple question - or so we thought. We wanted to know how the attitude towards a company could impact its stock's value. It turns out that question brings a lot more weight than we could have anticipated:

- Finding companies in headlines is *hard* - it's a developing part of NLP!
- Generalizing sentiment for a day helps us get around that, but it skews our evaluation of individual components (the headlines about a different company doesn't impact all others!)
- Many models aren't perfect, but there are some that might hold some promise.

While our models were far from perfect, there's a lot more that can be done. Working on better named entity extraction would be the first step. If we can't isolate that a headline is related to a specific company or industry, then there's not much sentiment can tell us other than how the general market may be doing. Working on optimizing 


## The bigger picture
--------------
Getting a value that's better than chance is a great starting point to help decide how and when to make a decision. 

<div align=center>
  <img src="/GaggleOfKaggle/img/NetworkStruct.png" width=400>
  <div class="caption">Our neural network had two hidden layers - one of 40 nodes and another of 2</div>
</div>
