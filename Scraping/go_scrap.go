package main

import (
	"encoding/csv"
	"github.com/gocolly/colly"
	"github.com/gocolly/colly/debug"
	"log"
	"os"
	"regexp"
	"sync"
)

type CsvWriter struct {
	mutex     *sync.Mutex
	csvWriter *csv.Writer
}

func SafeCsvWriter(fileName string) (*CsvWriter, error) {
	csvFile, err := os.Create(fileName)
	if err != nil {
		return nil, err
	}
	w := csv.NewWriter(csvFile)
	return &CsvWriter{csvWriter: w, mutex: &sync.Mutex{}}, nil
}

func (w *CsvWriter) Write(row []string) {
	w.mutex.Lock()
	w.csvWriter.Write(row)
	w.mutex.Unlock()
}

func (w *CsvWriter) Flush() {
	w.mutex.Lock()
	w.csvWriter.Flush()
	w.mutex.Unlock()
}

func main() {
	writer, err := SafeCsvWriter("data.csv")
	if err != nil {
		log.Fatal("Failed to make data file")
	}
	defer writer.Flush()

	writer.Write([]string{"Date", "Headline"})

	c := colly.NewCollector(
		colly.Debugger(&debug.LogDebugger{}),
		colly.Async(true),
		colly.CacheDir("./cache"),
	)

	headline_selector := "h3>.view-textlink>a"
	next_pge_selector := "a[aria-label=\"Next page\"]"
	next_dte_selector := ".archive-nav>a.next"

	c.OnHTML(headline_selector, func(e *colly.HTMLElement) {
		log.Println("Yes")
		link := e.Attr("href")
		text := e.Text

		re := regexp.MustCompile("([0-9]{4}-[0-9]{2}-[0-9]{2})")
		date := re.FindString(link)
		writer.Write([]string{date, text})
	})

	c.OnHTML(next_pge_selector, func(e *colly.HTMLElement) {
		e.Request.Visit(e.Attr("href"))
	})

	c.OnHTML(next_dte_selector, func(e *colly.HTMLElement) {
		e.Request.Visit(e.Attr("href"))
	})

	c.Visit("http://www.abc.net.au/news/archive/?date=2006-01-01")
	c.Wait()
}
