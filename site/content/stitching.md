+++
date = "2018-04-20"
draft = false
title = "Stitching Data"
weight = 4
type = "post"
+++

> How does daily overall sentiment affect the value of an industry?

When trying to answer a question about effect of one dataset on another, it necessitates the joining of the two. As a result, our next step was to combine our ticker data with the headline data itself, associating each company with a headline so we could see how the sentiment express impacted the value of their stock for that date. This task is much more involved than first meets the eye, as one data set includes the fully qualified name of a company (i.e. `QANTAS AIRWAYS LIMITED`) while the other uses their names in a more colloquial manner within a sentence (i.e. `security tightens for qantas in response to recent events`). This presents challenges such as:

- How to match abbreviated or partial company names?
- How to distinguish a true match from a false match (ie matching "security" instead of "quantas")?
- How to tell the difference between two company names given a context? (ie 'bell solutions' compared to 'bell technologies').

Solution 1: Fuzzy Matching
----------------------------

One popular way for finding a string within another string is through the usage of fuzzy matching, where a series of strings don't need to perfectly match your search term but be arbitrarily close to qualify as a match. This can help find different spellings of names such as `Walmart` vs `Wal-Mart` vs `Wal* Mart`. In our attempt we brought in the library [FuzzyWuzzy](https://github.com/seatgeek/fuzzywuzzy) to see what we could achieve.

``` python
def fuzzy_match(x, choices, scorer, cutoff):
    return process.extractOne(x, choices=choices, scorer=scorer, score_cutoff=cutoff)

def appfun(df):
    return df.loc[:FIRSTN, 'headline_text'].progress_apply(
        fuzzy_match,
        args=(ticker.loc[:, 'company'], fuzz.partial_ratio, 80)
    )

# Run in parallel
matching_results = parallelize(headlines, appfun)
```

We found this approach led to a lot of false matches due to longer substrings in headlines that matched part of a company name was valued more than a unique identifier in the company name ('quantas' wasn't matching better than the generic term 'solutions'). After toying with various fuzzy matching configurations our results weren't improving and the time to run the entire process was growing, eventually requiring us to write parallelization code to process chunks of the entire dataset on different CPU threads (8-Cores).

To address this we tried several NLTK approaches combined with the Fuzzy Matching, with the thought being we should remove non-nouns from the headlines to reduce the chances of non-name words from matching with our names. This would, in theory, only keep important terms necessary for matching. To speed up time, we also filtered out headlines that contained no parts of any company names (thus informing us we wouldn't be able to create a match at all). 

``` python
def fuzzy_match(x, choices, scorer, cutoff):
    tags = nltk.tag.pos_tag(x.split())
    filtered = " ".join([x[0] for x in tags if x[1] in nouns])
    if filtered == '':
        return
    return process.extractOne(filtered, choices=choices, scorer=scorer, score_cutoff=cutoff)
```

This approach dramatically reduced matches that shouldn't have been paired at all, but took 4-5 hours to run and still was producing poor matches when a match was made. We also found that NLTK wasn't able to identify Nouns quite right, due to its need for sentences to have proper grammar (so Proper Nouns, for example, should be capitalized). Since the author of our dataset decided to lowercase all strings, we lost this critical information NLTK needed to properly process phrases.

Solution 2: Position Based Matching
----------------------------

With this in mind we tried a more custom algorithm for matching instead of fuzzy matching that tried to weigh terms in a company's name by the rank within the title. For example, when matching "QANTAS AIRWAYS LIMITED" the algorithm would value a match of "Qantas" more than if the next word "Airways" matched, and it would weigh "LIMITED" even lesser. This would encourage "Qantas" to reign as the correct match rather than if another company with the term "limited" had matched. We sped this computation up by creating sets out of the terms in both headlines and company names, and then performing set intersection to determine if words matched. Even after all of that, however, results were poor and slow. Below is the abbreviated algorithm, giving you the gist of what it was doing.

``` python
# 1. Make sets from companies and headlines in their stripped form.
ticker['company_set'] = ticker['company'].apply(lambda x: set(normalize(x)))
# ...
def findMatches(headline):
    # ...
    for company in ticker:
        # ...
        # 2. Intersect headline with each company, assign score 
        # with matching terms weighted on position in company name
        shared = headlineSet & companySet
        if len(shared) > 0:
            for word in shared:
                companyMatchScore += (1/(WordIndexInCompanyName+1))
        # 3. Normalize the score based on its company length, to give every
        # company a fair chance for matching.
        normalizedScore = companyMatchScore / len(companySet)
    # ...
```

This made unique company name matches work really well, like "Qantas", but failed in most other cases. It also ran within a reasonably okay time frame, but we still weren't getting good results. We tried combining this approach with the noun-extraction of NLTK, but in the end, we decided to try another solution.

Solution 3: Scrape the Data
----------------------------

Given what we really wanted to find was the subject of each sentence we knew we needed to have our headlines in proper grammatical form. To solve this we ended up rescraping our data from the ABC Archives. This meant we could only go as far back as 2006, but we could at least get well-formed data. We did this with the ScraPy library, which is a more powerful version of BeautifulSoup one may argue designed to crawl from page to page while adhering to the Robots.txt of the sites it visits.

``` python
class NewsScraper(scrapy.Spider):

  def __init__(self):
    self.start_urls = ['http://www.abc.net.au/news/archive/?date='+self.getdate()]

  def parse(self, response):
    # Grab all the headlines from the current day
    TITLE_SELECTOR = 'h3 >.view-textlink > a ::text'
    for headlines in response.css(TITLE_SELECTOR):
        yield {
          'date': self.getdate(),
          'titles': headlines.extract()
        }

    if next_page:
      # If this day had another page, go to it first
      yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
    elif next_date:
      # Otherwise go to the next day's headlines
      self.current_date = datetime.strptime(next_day, '%a %d %b, %Y').date()
      if self.current_date >= self.end_date:
        # Stop if this day is past our enddate, however.
        return

      yield scrapy.Request( response.urljoin(next_date),callback=self.parse)
```

The above code is more or less the entirety of the scraper - it turns out ScraPy is very easy to use! We ran this code on a Raspberry Pi and 4 days later had all of our headlines. Four days sounds like the process was slow, but the Robots.txt of ABC requested that all scrapers wait 5 seconds between making requests, which meant we were limited not by processing power.

After scraping the data, no preprocessing had to be done beyond stripping excess whitespace from the ends of the headlines. We took this and ran it back through Solutions 1 and 2 of this post, sadly finding performance was still sub-par. It turns out NLTK was still struggling to identify nouns very well. Upon this realization we came across another NLP library for Python called SpaCy. SpaCy had the key differences that it was designed for Named Entity Recognition as one of its core functions (through using a combination of word vector analysis and known dictionary of entities). Using this we found huge success in identifying subjects of sentences:

``` python
for doc in nlp.pipe(sample_test['titles'].astype('unicode').values, batch_size=50,
                        n_threads=3):
    if doc.is_parsed:
        subjects.append([tok for tok in doc if (tok.dep_ == "nsubj")])
        orgs.append([ent.text for ent in doc.ents if (ent.label_ == "ORG")])
    else:
        # We want to make sure that the lists of parsed results have the
        # same number of entries of the original Dataframe, so add some blanks in case the parse fails
        subjects.append(None)
        orgs.append(None)

sample_test['subject'] = subjects
sample_test['orgs'] = orgs
sample_test.head(500)
```

<div align=center>
  <img src="/GaggleOfKaggle/img/subject_identification.png">
  <div class="caption">SpaCy was really good at finding subjects</div>
</div>

This solution was also much faster, taking approximately 8 minutes in a threaded workload to process most of the data. We then could use SpaCy's similarity functionality to match to our companies:

``` python
def find_most(word):
    max_sim = ('', 0)
    if type(word) is list:
        for token in word:
            for company in companies:
                company = nlp(company)
                sim = token.similarity(company)
                if sim > max_sim[1]:
                    max_sim = (company, sim)
    else:
        for company in companies:
            company = nlp(company)
            sim = word.similarity(company)
            if sim > max_sim[1]:
                max_sim = (company, sim)
    return max_sim
sample_test['subject_sim'] = sample_test['subject'].apply(find_most)
sample_test.head(500)
```

Yet even with that, we still failed to find matches reliably. Having solved the core issue of identifying entities within our headlines, we still couldn't match our two list of entities. The largest reason being that our list of entities were their full names and not their colloquial names, which meant that since headlines weren't using the entire name of a corporation we couldn't get reliable matches. The only solution from here would have been to rebuild our list of companies using common namings of them rather than their full names, but given we were now short for time, this really wasn't an option. Converting such a list would require knowledge of how a company may be referred to or some list of alternative names that we did not possess. As a final solution, we decided to alter our question slightly:

> Instead of asking how sentiment might affect a **company's** value, we now asked how might a day's net sentiment affect an **industry's** value.

This made it possible to now join our data on dates instead of companies.