import requests
import re
from pandas import DataFrame
import matplotlib.pyplot as plt
from pymongo import MongoClient
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from scipy.sparse import coo_matrix
from collections import Counter
nltk.download('stopwords')
nltk.download('wordnet')

# MongoDB Connection
client = MongoClient('mongodb+srv://root:root@crawlertheguardian-sjvep.mongodb.net/crawlertheguardian?retryWrites=true&w=majority')
#Name of Database
db = client['crawlertheguardian']

#recovery of articles
def articles_of_mongodb():
    # list of articles
    articles = []
    #get of articles the collection  articles
    col = db.get_collection("articles")
    for document in col.find({}):
        # add document in list of articles
        articles.append(document)
    #dataset=pd.DataFrame(articles)
    return articles


#text Preprocessing
def Preprocessing():
    #recovery of articles
    dataset=articles_of_mongodb()
    # Save articles in dataframe format
    dataset=pd.DataFrame(dataset)
    # get a full list for english language
    stop_words = set(stopwords.words("English"))
    # Delete of spaces between words
    text=dataset['text'].apply(lambda x: (str(x).split ("  ")))
    content=[]
    corpus = []

    s = ', '
    for i in range(0,len(text)):
        sen=[]
        for x in text[i]:
        # Delete of space between caracters
            x=x.replace(" ","")
            sen.append(x)

        se=s.join(sen)
        # Delete of comma between caracters
        se=se.replace(",","")
        content.append(se)

    keyword=[]
    corpus = []
    for i in range(0, len(content)):
        #Remove punctuations
        text = re.sub('[^a-zA-Z]', ' ', content[i])

        #Convert to lowercase
        text = text.lower()

        #remove tags
        text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)

        # remove special characters and digits
        text=re.sub("(\\d|\\W)+"," ",text)

        ##Convert to list from string
        text = text.split()
        ps=PorterStemmer()
        #Lemmatisation
        lem = WordNetLemmatizer()
        text = [word for word in text if not word in stop_words] 
        text = " ".join(text)

        corpus.append(text)
    return corpus

# recovery of the 10 keywords of a sentence
def keywords(phrase):
    words = [word for word in phrase.split()]
    # get the 10 keywords of a sentence
    wordcount = Counter(words).most_common(10)
    keywords=dict(wordcount)
    return list(keywords.keys())

#Retrieving keywords from article text 
def list_keyword():
    #get of articles the collection  articles
    dataset=articles_of_mongodb()
    #Save list of articles in dataframe format
    dataset=pd.DataFrame(dataset)
    liste=[]
    # text Preprocessing 
    articles=Preprocessing()
    for i in range(0,len(articles)):
        liste.append(keywords(articles[i]))
    return(liste)

#Save articles in dataframe format   
def dataframe_news():
    #get of articles the collection  articles
    articles=articles_of_mongodb()
    #Save list of articles in dataframe format
    dataset=pd.DataFrame(articles)
    # text Preprocessing 
    text=Preprocessing()
    keyword_list=list_keyword()
    list_keywords=keyword_list
    text_cleaner=pd.DataFrame({'text_cleaner':text,'list_keywords':list_keywords})
    dataset=dataset.join(text_cleaner)
    return dataset

# Retrieving articles by keyword
def getArticles(keyword):
    #get of articles the collection  articles
    dataset=articles_of_mongodb()
    #Save list of articles in dataframe format
    dataset=pd.DataFrame(dataset)
    dataset=dataframe_news()
    data=dataset[dataset['list_keywords'].apply(lambda x : any((i for i in x if i.find(keyword) >= 0 )))]
    # return of list of articles in dataframe format
    return data[['_id','headline','author','text','url']]
