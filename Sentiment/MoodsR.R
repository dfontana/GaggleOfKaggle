library(SentimentAnalysis)
library(readr)
data = read_csv("C:/Users/Stephanie/DS3001/abcnews-date-text.csv")
data = data.frame(data)
data$date = as.Date(as.character(data$date), format = "%Y-%m-%d")

start <- as.Date("01-08-14",format="%d-%m-%y")
end   <- as.Date("08-09-14",format="%d-%m-%y")

theDate <- start

while (theDate <= end)
{
    yr03 = data[data$date >= "2018-01-01" & data$date < "2018-03-01",]
    headlines = yr03[,"titles"]
    sentiment = analyzeSentiment(headlines)
    directions = convertToDirection(sentiment$SentimentQDAP)
    write.table(directions, file="rsentiments.csv", sep=",", col.names = FALSE,row.names=FALSE, append=TRUE)
    theDate <- theDate + 90
}



