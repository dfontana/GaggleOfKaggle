library(SentimentAnalysis)
library(readr)

sent = function(headlines){
  sentiment = analyzeSentiment(headlines)
  scores = sentiment$SentimentQDAP
  return(sentiment)
}
