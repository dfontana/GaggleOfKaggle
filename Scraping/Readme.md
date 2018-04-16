# Scraping

Two options for scraping, one happens to be faster than the other with slightly less control.

## Option 1: Scrapy & Python

With the Python library Scrapy, you can run the scraper.py file to fetch the raw headline data. Inside the script are a start and end date, edit those to define the bounds in which to scrap data from. You'll want to run this file as `scrapy runspider scraper.py -o data.csv`, which will automagically output the scraper's data to a CSV. You'll need to have scrapy installed: `pip install scrapy`.

The downside to this option, is the scraper runs on a single thread so it might be a little slower since it does one call at a time.

## Option 2: Colly & Go

With the Golang library Colly, you can run the go_scrap.go file to fetch the raw headline data. This one differs from the Python option in that it does not have a controllable end date setup (but you can edit the starting URL to point it at a starting time). It also runs Asynchronously, allowing multiple threads to execute at a time. This speeds things up, as new pages can be requested while others are still being parsed. This Asynchronous behavior, however, means that the end date can't be controlled easily (as is structured) and the outputted CSV is not sorted. The latter of these two problems is very easily solved with the following linux command: `sort data.csv -k 1`.

You'll either need to `go get -u github.com/gocolly/colly` and then either build the executable (`go build`) or just run the script `go run go_scrap.go`.
