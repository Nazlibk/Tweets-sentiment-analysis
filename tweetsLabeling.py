""" This file is used to labeling the tweets. As our approaches are supervised learning we need to have labeled data.
We have three labels. 2: strong signal, 1: weak signal, 0: no signal
Then, these labeled data will used for training the models.
"""

import pandas as pd
from flashtext import KeywordProcessor
import csv

# Importing the dataset
dataset = pd.read_csv('tweets.csv')
dataset['label'] = 0
# Creating keywords list
keywords = ['CEO', 'CFO', 'extend', 'expand', 'raise', 'increase', 'hike', 'international', 'invest', 'investment',
            'sign', 'contract', 'foreign', 'partner', 'global', 'investor', 'outside', 'Asian', 'Nations', 'Europe',
            'Americas', 'sale', 'abroad', 'customers', 'new',  'product', 'item', 'service', 'stake', 'buy', 'millions',
            'billions', 'shareholder', 'dollars', 'euros', 'pounds', '$', 'deal', 'Entrepreneur', 'office', 'growth',
            'strategy', 'network', 'exchange', 'rate', 'fluctuation', 'venture', 'trade', 'transaction', 'pact', 'sell',
            'profit', 'loss', 'revenue', 'quarter', 'results', 'acquisition', 'agreement', 'acquire', 'agreement',
            'addition', 'capital', 'organisation', 'establishment', 'inauguration', 'foundation', 'formation',
            'commencement', 'launch', 'onset', 'start', 'kickoff', 'setup', 'package', 'winning', 'gaining', 'purchase',
            'win', 'bargain', 'currency', 'conversion', 'small', 'scale', 'medium', 'business', 'opportunity', 'economy',
            'transfer', 'start-up', 'MoU', 'announcement', 'committee', 'collaboration', 'eu', 'uk', 'gbp', 'usd', 'us',
            'irish', 'market', 'tender','sanction', 'arrangement']


# Find the roots of the keywords
from nltk.stem.porter import PorterStemmer
porter_stemmer = PorterStemmer()
keywords_root = []
for w in keywords:
       keywords_root.append(porter_stemmer.stem(w))
keywords_root = list(set(keywords_root))


# This method is go through each tweets and count how many of the keywords exist in the tweet text.
from tokenizing import preprocess
def labeling(text):
    processor = KeywordProcessor()
    processor.add_keywords_from_list(keywords_root)
    words = preprocess(text)
    # Find the roots of words in the text
    words_root = ""
    for w in words:
        if type(w) != float:
            words_root = words_root + porter_stemmer.stem(w) + " "
    # Searching for keywords in the text
    found = processor.extract_keywords(words_root)
    return found

# This method writes labeled data in a CSV file
def write_on_file():
    fileName = "labeledTweets3Classes.csv"
    f = csv.writer(open(fileName, "w+"))
    # Write CSV Header
    f.writerow(["hashtags", "text", "retweeted", "location", "name", "screen_name", "label"])

    for _, row in dataset.iterrows():
        f.writerow([row["hashtags"],
                    row["text"],
                    row["retweeted"],
                    row["name"],
                    row["location"],
                    row["screen_name"],
                    row["label"]])

for index, row in dataset.iterrows():
    found = labeling(row['text'])
    # Label the tweet as 0 (means no signal) if none of the keywords are exist in the tweet text
    if(len(found) == 0):
        dataset['label'][index] = 0
    # Label the tweet as 1 (means weak signal) if just one of the keywords are exist in the tweet text
    elif(len(found) == 1):
        dataset['label'][index] = 1
    # Label the tweet as 2 (means strong signal) if two or more of the keywords are exist in the tweet text
    else:
        dataset['label'][index] = 2

write_on_file()

