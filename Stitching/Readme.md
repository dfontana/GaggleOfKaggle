# Stitching

Here is a quick list of the item tried thus far to stitch the Stock data to the Headline data

## 1: FuzzyWuzzy

The library `fuzzywuzzy` was brought in as an effort to fuzzy match company names to within the headlines. This was done using a partial ratio match (meaning if part of the company name appeared, its ratio would be scored rather than requiring a strict match). Given abbreviations of company names exist, this option didn't work too well as companies don't go by their full name or companies with longer substrings present in a headline were getting falsely matched to headlines.

It should also be noted that things were very slow at this point. Using `tqdm` I was able to estimate the runtime of stitching the entire dataset, and things were looking at 4 hours timing. Not horrible, but bad. I parallelized the code using a Processing pool of worker threads, which dropped timing to 2 hours.

## 2: NLTK + FuzzyWuzzy

To help with the false matching problem, I tried filtering out non-noun words within the headlines using NLTK. This would isolate only the important names within the string (in theory) and thus make fuzzy matching more accurate. The two problems that occured were 1) the headlines were all lowercase, so NLTK could not exploit caitalization to easily identify names. This made it semi-effective at best for isolating proper nouns. 2) the issue of headlines having false matches got somewhat better since there were less trash words within the headlines to falsely match, but it still was occuring with an unacceptable rate.

Timing wise, this exacerbated the issue raising the time to 12 ish hours (or something in the teens). The parallelization code helped reduce this down to 4-5 hours, which is barely okay.

## 3: Custom Strict Search

Using our own algorithm, we attempted to find names that matched the most components of a company's full name, weighting each sequential word in the name as less valuable than the prior. This made first word matches much more valueable and found strong success with uniquely named companies. For example "quantas" would match with a high accuracy, since its first word match prevented longer substring matches from outweighing it.

The problem with this approach was that companies were not being found if they had an abbreviation or more than one company matched to a headline. Runtime was also up to 33 hours.

## 4: Custom Strict Search + Set Intersection + Filter

To help speed the process, the headlines were filtered to remove those that did not have any company name components present. This reduced the dataset to 75% (ish) of its size. Then, instead of searching for substrings, headlines and company names were converted to sets (and stored ahead of time). While checking each string we then Set Intersected a headline and company set, determining which words match must faster. We then determine the index of these words in the company name to assign the weight. 

Timing wise this was effective at reducing it down much more (I can't recall exact hours), but we still weren't getting good matches.

## 5: Rescrape + NLTK + FuzzyWuzzy

Given we really needed to isolate proper nouns to be effective, we opted to rebuild the dataset we found from kaggle by writing our own scraper in ScraPy. We then ran the scraper for 4 days on a RaspberryPi, pulling headline data from the Australian Broadcasting Company archive. 

After which, we lightly trimmed whitespace, used NTLK to isolate Proper Nouns, filtered headlines that only contained company names, and then used FuzzyWuzzy to perform a match.

... Results not yet in on effectiveness.





