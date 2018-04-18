import pandas as pd
import numpy as np
from tqdm import tqdm_notebook, tqdm
import nltk
from pathlib import Path
import string


# Load data, clean it
ticker = pd.read_csv('../data/asx-tickers.csv')
combined_headlines = Path('../data/scraped/combined_headlines.csv')
if not combined_headlines.is_file():
    head_1 = pd.read_csv('../data/scraped/2006_2010.csv')
    head_2 = pd.read_csv('../data/scraped/2010_2010.csv')
    head_3 = pd.read_csv('../data/scraped/2010_2016.csv')
    head_4 = pd.read_csv('../data/scraped/2016_2017.csv')
    headlines = head_1.append([head_2, head_3, head_4])
    headlines.to_csv('../data/scraped/combined_headlines.csv')
headlines = pd.read_csv('../data/scraped/combined_headlines.csv')
stripped = headlines.titles.apply(lambda x: x.strip('"\' ' ))
headlines_clean = headlines[~headlines.titles.duplicated(keep='first')]


# Filter the headlines only relevant
translator = str.maketrans('','',string.punctuation)

def normalize(s):
    return s.lower().translate(translator).split()

def incompwords(s):
    headwords = set(normalize(s))
    return len(headwords & compwords) > 0

compwords = set(normalize((" ".join(ticker['company'].values))))
headlines_filtered = headlines_clean[headlines_clean.titles.apply(incompwords)]


# Isolate the Entities
nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def extract_entity_names(t):
    entity_names = []

    if hasattr(t, 'label') and t.label:
        if t.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))

    return entity_names

def identify_entities():
    f = headlines_filtered.titles.tolist()
    matches = []
    for line in tqdm(f, total=len(f), unit="headlines"):
        sentences = nltk.sent_tokenize(line)
        tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
        tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
        chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

        entities = []
        for tree in chunked_sentences:
            entities.extend(extract_entity_names(tree))
            
        if len(entities) == 0:
            matches.append(np.nan)
        else:
            matches.append(", ".join(entities))

    series = pd.Series(matches)
    out = headlines_filtered.copy()
    out['entities'] = series.values
    out = out.dropna()
    out.to_csv("../data/headline_entity_id.csv")
    
entitymatch = Path('../data/headline_entity_id.csv')
if not entitymatch.is_file():
    identify_entities()
headline_entities = pd.read_csv("../data/headline_entity_id.csv")


# Threaded code
from multiprocessing import cpu_count, Pool
cores = cpu_count()
def parallelize(data, func):
    data_split = np.array_split(data, cores)
    pool = Pool(cores)
    data = pd.concat(pool.map(func, data_split))
    pool.close()
    pool.join()
    return data



# Thread safe writing
import threading
import csv
csv_writer_lock = threading.Lock()
match_file = open('../data/position_match.csv', "wb")
writer = csv.writer(match_file, ['date', 'titles', 'entities', 'matches'])

def write_to_csv(row):
  print(row)
  with csv_writer_lock:
    writer.writerow(row)
  
# Positional Matching
tick_df = ticker.copy();
tick_df['set'] = tick_df['company'].apply(lambda x: set(x.title().split(" ")))
tick_df['list'] = tick_df['company'].apply(lambda x: x.title().split(" "))
MIN_SCORE = 0.3
def findMatches(headline):
  matchedCompanies = []
  if headline['entities'] == '' or type(headline['entities']) != str:
    return
  entity_set = set(headline['entities'].split(', '))
  for _,company in tick_df.iterrows():
    companyMatchScore = 0
    company_set = company['set']
    shared = entity_set & company_set
    if len(shared) > 0:
      for word in shared:
        idx = company['list'].index(word)
        companyMatchScore += (1/(idx+1))
    normalizedScore = companyMatchScore / len(company_set)
    if normalizedScore >= MIN_SCORE:
      matchedCompanies.append((company['company'], normalizedScore))
  matchedCompanies.sort(key=lambda x: x[1], reverse=True)

  write_to_csv({
    'date':headline['date'],
    'titles':headline['titles'],
    'entities':headline['entities'],
    'matches': ", ".join([str(tup) for tup in matchedCompanies[:10]])
  })

  return matchedCompanies[:10]


# Run the Matching & output
tqdm.pandas(desc="Position Match")
def appfun(df):
    return df.progress_apply(findMatches, axis=1)
matching_results = parallelize(headline_entities, appfun)
match_file.close()