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

import scrapy
from datetime import date, datetime

class NewsScraper(scrapy.Spider):
  start_date = date(2016,1,1)
  end_date = date(2017,12,31)
  current_date = start_date
  name = "abcnews_spider"

  def __init__(self):
    self.start_urls = ['http://www.abc.net.au/news/archive/?date='+self.getdate()]

  def parse(self, response):

    TITLE_SELECTOR = 'h3 >.view-textlink > a ::text'
    for headlines in response.css(TITLE_SELECTOR):
        yield {
          'date': self.getdate(),
          'titles': headlines.extract()
        }

    NEXT_PAGE_SELECTOR = 'a[aria-label="Next page"] ::attr(href)'
    NEXT_DATE_SELECTOR = '.archive-nav>a'

    next_date_ele = response.css(NEXT_DATE_SELECTOR)

    next_day = next_date_ele.css('::text').extract_first().strip(' \t\n\r')
    next_date = next_date_ele.css('::attr(href)').extract_first()
    next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()

    if next_page:
      yield scrapy.Request(
        response.urljoin(next_page),
        callback=self.parse
      )
    elif next_date:
      self.current_date = datetime.strptime(next_day, '%a %d %b, %Y').date()

      if self.current_date >= self.end_date:
        # Stahp.
        return

      yield scrapy.Request(
        response.urljoin(next_date),
        callback=self.parse
      )


  def getdate(self):
    return self.current_date.strftime('%Y-%m-%d')