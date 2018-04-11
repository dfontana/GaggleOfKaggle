library(SentimentAnalysis)
library(readr)
data = read_csv("C:/Users/Stephanie/DS3001/abcnews-date-text.csv")
data = data.frame(data)
data$publish_date = as.Date(as.character(data$publish_date), format = "%Y%m%d")
yr03 = data[data$publish_date >= "2018-01-01" & data$publish_date < "2018-03-01",]
headlines = yr03[,"headline_text"]

sentiment = analyzeSentiment(headlines)
directions = convertToDirection(sentiment$SentimentQDAP)
write.table(directions, file="rsentiments.csv", sep=",", col.names = FALSE,row.names=FALSE, append=TRUE)

