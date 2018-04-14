import scrapy

"""
http://www.abc.net.au/news/archive/?date=2006-01-01&page=5

https://www.digitalocean.com/community/tutorials/how-to-crawl-a-web-page-with-scrapy-and-python-3

Notes: 

Date format: YYYY-MM-DD
Headlines CSS: h3>.view-textlink>a
Next page CSS: a[aria-label="Next page"]

Start date: 2006-01-01
End date: 2017-12-31

Logic:

currentDate = startDate
while(currentDate != startDate){
  page = 1
  do{
    fetch page for currentDate
    get all titles, write to disk
    page++
    pause(5 secs)
  }while(NEXT BUTTON EXISTS)
  currentDate++
}

Run: scrapy runspider scraper.py
"""

class NewsScraper(scrapy.Spider):
    name = "abcnews_spider"
    start_urls = ['http://www.abc.net.au/news/archive/?date=2006-01-01']

    def parse(self, response):
        TITLE_SELECTOR = 'h3 >.view-textlink > a ::text'
        for headlines in response.css(TITLE_SELECTOR):
            yield {
              'titles': headlines.extract(),
              'date': 
            }