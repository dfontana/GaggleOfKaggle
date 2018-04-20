library(SentimentAnalysis)
library(readr)
data = read_csv("../data/scraped/combined_headlines.csv")
data = data.frame(data)
data$date = as.Date(as.character(data$date), format = "%Y-%m-%d")

start <- as.Date("2006-01-01",format="%Y-%m-%d")
end   <- as.Date("2017-12-30",format="%Y-%m-%d")

prevDate <- start
nextDate <- start + 90

while (prevDate <= end)
{
    print(format(prevDate,"%Y-%m-%d"))
    print(format(nextDate,"%Y-%m-%d"))
    yr03 = data[data$date >= format(prevDate,"%Y-%m-%d") & data$date < format(nextDate,"%Y-%m-%d"),]
    headlines = yr03[,"titles"]
    sentiment = analyzeSentiment(headlines)
    sentiment$direction <- convertToDirection(sentiment$SentimentQDAP)
    write.table(sentiment, file="test_rsentiments.csv", sep=",", col.names = FALSE,row.names=FALSE, append=TRUE)
    prevDate <- nextDate + 1
    nextDate <- prevDate + 90
}
