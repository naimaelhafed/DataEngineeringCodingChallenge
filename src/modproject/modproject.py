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



if __name__ == "__main__":
    print(articles_of_mongodb())