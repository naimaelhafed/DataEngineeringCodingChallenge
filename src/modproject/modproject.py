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
#nltk.download('stopwords')
#nltk.download('wordnet')

# MongoDB Connection
client = MongoClient('mongodb+srv://root:root@crawlertheguardian-sjvep.mongodb.net/crawlertheguardian?retryWrites=true&w=majority')
db = client['crawlertheguardian']

#recovery of articles
def articles_of_mongodb():
    articles = []
    col = db.get_collection("articles")
    for document in col.find({}):
        articles.append(document)
    #dataset=pd.DataFrame(articles)
    return articles


#text Preprocessing
def Preprocessing():
    dataset=articles_of_mongodb()
    dataset=pd.DataFrame(dataset)
    stop_words = set(stopwords.words("English"))
    text=dataset['text'].apply(lambda x: (str(x).split ("  ")))
    content=[]
    corpus = []

    s = ', '
    for i in range(0,len(text)):
        sen=[]
        for x in text[i]:
            x=x.replace(" ","")
            sen.append(x)

        se=s.join(sen)
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


if __name__ == "__main__":
    #print(articles_of_mongodb())
    print(Preprocessing())