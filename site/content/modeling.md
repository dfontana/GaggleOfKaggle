+++
date = "2018-04-28"
draft = false
title = "Creating Models"
weight = 5
type = "post"
+++

> How does daily overall sentiment affect the value of an industry?

With our datasets now joined we could make a series of models that would attempt to predict the value of a stock based on sentiment. We tried three types: Support Vector Regression, Support Vector Machine, and a Multilayer Perceptron (Neural Network). These models were based on either individual companies (so just predicting one company's stock) or individual industries (like predicting the value of Food & Beverage). Our results are shown in the table below.

Type                          | Focus    | Result
------------------------------|----------|--------------
Support Vector Regression     | Company  | R2 = -10.22
Support Vector Machine        | Company  | Acc = 53.8%
Neural Network                | Company  | Acc = 57.78%
Support Vector Machine        | Industry | Acc = 61.92%
Neural Network                | Industry | Acc = 62.17%

## Training Data
-----------------

All of the models had their training data prepared in roughly the same way. This preprocessing was done with Pandas and [SciKit-Learn](http://scikit-learn.org/stable/). The sentiments were loaded in, along with the tickers and stock data. The stock data went through a preprocessing step that computed the difference from the prior day's value. 

<div align=center>
  <img src="/GaggleOfKaggle/img/stock_diff_data.png">
  <div class="caption">Stock Data with differences from close-to-open and close-to-close</div>
</div>

This value then was encoded as a 1 if it was positive (the stock increased) or a 0 if it was negative (the stock decreased). The stocks were then joined with the tickers. After this the sentiment data was offset by one day, such that the prior day's sentiment's date would align with the current day, and then joined with stock data.

<div align=center>
  <img src="/GaggleOfKaggle/img/training_data.png">
  <div class="caption">The final training structure</div>
</div>

Depending if the model was a company or an industry, the next step would either filter the ticker column for just the records related to a specific company or filter the industry column for just a particular industry. In our testing we used the company Qantas and the Food, Beverage, & Tobacco industry to train out models. We then used SciKit's `train_test_split()` to divide the dataframe into 80% training data and 20% testing data. 

## Support Vector Regression
------------------------------

In a support vector regression, a function is fitted to the training data such that it approximates the output value as closely as possible. One benefit of this is that predicted values are continuous, allowing a more precise prediction to occur on the stock's value than just "increase" or "decrease". A strong regression would have a high R-Squared value, however, and we only trained one of these models as we found it performed very poorly - almost as expected. The variation within the data is too high to fit a function to accurately. As a result you get something that looks like this:

<div align=center>
  <img src="/GaggleOfKaggle/img/svr.png">
  <div class="caption">The poor fit of an SVR</div>
</div>

The R-Squared of this model was -10.22. Not only is it very low, but it's negative which shows the fit is worse than a horizontal line.

## Support Vector Machine
-----------------------------

In a support vector machine, lines are fitted into space in effort to classify data points. These lines are called "Support Vectors" and they are formed during training time. Future inference then places new points into the space and classify them within whatever region of space they fall within. These vectors can be straight lines, polynomials, or higher order functions taking on abstract shapes. Since this is a classification based problem, we can evaluate a model based on its accuracy. We found this type of model to perform better than an SVR - sitting around 53%-61% accuracy depending on if it was company or industry. The spaces, however, tell us much more:

<div align=center>
  <img src="/GaggleOfKaggle/img/svm_company.png" width=400>
  <img src="/GaggleOfKaggle/img/svm_industry.png" width=400>
  <div class="caption">What the SVM space looks like for a company (left) and an industry (right)</div>
</div>

*This is why data visualization is so key!* While 53%-61% accuracy isn't horrendous (it's slightly better than chance), we can see from visualizing the model that is actually is much *worse*. Neither SVM is really fitting to the data, but rather selectively grabbing a few data points out of the larger group, in a more hap-hazard manner.

## Neural Network
-----------------------------

The final models we tried were very simple Neural Networks (Multilayer Perceptrons) built from SciKit-Learn's MLPClassifier. A Neural Network, in a few words, attempts to learn patterns found in the data it sees. This is a classic form of Supervised Learning. As it sees more and more new inputs, the network will update the numeric values inside itself called weights. These weights essentially determine how much individual neurons (typically denoted as circles) get to have a say in the final classification.

For our network, the structure looked as such:

<div align=center>
  <img src="/GaggleOfKaggle/img/NetworkStruct.png" width=400>
  <div class="caption">Our neural network had two hidden layers - one of 40 nodes and another of 2</div>
</div>

At a very high level (with lots of hand waving) the network works as follows. The input neuron received the prior day's sentiment. This value was fed into 40 neurons in the first layer (called a hidden layer). These 40 neurons processed the value, and after accounting for their weight, fed it to the next hidden layer of two neurons. Then these two fed into the output neuron.

We found a classification accuracy of 62% in the best case for this type of model. While there is much more that can be done in terms of trying alternate styles of neural networks (like Recurrent Neural Networks, which are suitable for time based data), there's more to be said about the model evaluation. Unlike the SVM, we can't easily plot this model's training to see if there's anything hidden in the details. Ideally we'd want to look at other evaluation metrics (such as F1-Score) and the graph of the training itself, to understand if the training converged or just happened to end at 62% accuracy.