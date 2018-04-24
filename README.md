# GaggleOfKaggle
Stock market data comparison to Australian headlines

# Task items:

Guiding Question:
- How does daily overall sentiment affect each industry's value.
 - What phrases or words spawned the large deviations an industry's value took? (For example, if an industry rose heavily on a date, why?)
 - Do these phrases reoccur on average?

Task items:
- Steph: [x] Prepare the R files and Python notebook for rerunning Sentiment Analysis on the updated headlines
 - [x] Adjust code to also include the numbers.
- Ranier: [ ] Determining stock data changes per date
    - [ ] Evaluate average relative (weighted by the overall stock value) change for each stock
    - [ ] Base it on the stock's closing value, not the others.
    - [ ] Do for each company first, then do the weighted aggreation per industry. Save as two seperate CSVs. CSVs should have date, ticker, and percent change.
- Steph: [x] Determine the overall sentiment per day from the headline data (export as CSV: date, overall summed, overall mode).
    - [x] Do the mode for the day
    - [x] Do the summed sentiment for the day
- [ ] Analysis of Daily Sentiment affect on each Company (2227) and Industry (26)
    - Owen: [ ] Correlate overall sentiment for a day and relative stock change (By company and by industry)
    - Owen: [ ] Logistic Regression setup. Input: Prior N day's sentiment, output next day's change. (By company and by industry). Cross Validate for final metric.
    - Dylan: [ ] Research SVM stuff. Input: Prior N day's sentiment, output next day's change. (By company and by industry). Cross Validate for final metric.
- Dylan: [ ] setup the blog and start filling it in.

Final Product:
- Blog post "esque", describing our results with some handy visuals, culminates in an attempt to show how well we could predict the next day.
- Visuals:
 - Word Cloud of common words
 - Correlations
 - Regressions
 - Predictive accuracies for model.
