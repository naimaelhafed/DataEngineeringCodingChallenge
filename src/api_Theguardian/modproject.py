import re
from collections import Counter
from pymongo import MongoClient
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('wordnet')

# MongoDB Connection
connexion = MongoClient('mongodb+srv://root:root@crawlertheguardian-sjvep.mongodb.net/crawlertheguardian?retryWrites=true&w=majority')
#Name of Database
name_database = connexion['crawlertheguardian']

#recovery of articles
def articles_of_mongoname_database():
    # list of articles
    articles = []
    #get of articles the collection  articles
    col = name_database.get_collection("articles")
    for document in col.find({}):
        # add document in list of articles
        articles.append(document)
    #dataset=pd.DataFrame(articles)
    return articles


#text preprocessing
def preprocessing():
    #recovery of articles
    dataset = articles_of_mongoname_database()
    # Save articles in dataframe format
    dataset = pd.DataFrame(dataset)
    # get a full list for english language
    stop_words = set(stopwords.words("English"))
    # Delete of spaces between words
    text = dataset['text'].apply(lambda x: (str(x).split("  ")))
    content = []
    corpus = []

    comma_space = ', '
    for i in range(0, len(text)):
        sentence = []
        for word in text[i]:
            word = word.replace(" ", "")
            sentence.append(word)

        sentences = comma_space.join(sentence)
        sentences = sentences.replace(",", "")
        content.append(sentences)

    corpus = []
    for i in range(0, len(content)):
        #Remove punctuations
        text = re.sub('[^a-zA-Z]', ' ', content[i])

        # Convert to lowercase
        text = text.lower()

        # remove tags
        text = re.sub("&lt;/?.*?&gt;", " &lt;&gt; ", text)

        # remove special characters and digits
        text = re.sub("(\\d|\\W)+", " ", text)

        ##Convert to list from string
        text = text.split()
        porterstemmer = PorterStemmer()
        #Lemmatisation
        lem = WordNetLemmatizer()
        text = [word for word in text if not word in stop_words]
        text = [porterstemmer.stem(word) for word in text]
        text = [lem.lemmatize(word) for word in text]
        text = " ".join(text)

        corpus.append(text)
    return corpus

# recovery of the 10 keywords of a sentence
def keywords_of_sentence(sentence):
    list_words = [word for word in sentence.split()]
    # get the 10 keywords of a sentence
    count_word = Counter(list_words).most_common(10)
    keywords = dict(count_word)
    return list(keywords.keys())

# Retrieving keywords from article text
def keywords_of_article():
    #get of articles the collection  articles
    dataset = articles_of_mongoname_database()
    #Save list of articles in dataframe format
    dataset = pd.DataFrame(dataset)
    liste = []
    # text preprocessing 
    articles = preprocessing()
    for i in range(0, len(articles)):
        liste.append(keywords_of_sentence(articles[i]))
    return liste

#Save articles in dataframe format
def dataframe_articles():
    #get of articles the collection  articles
    articles = articles_of_mongoname_database()
    #Save list of articles in dataframe format
    dataset = pd.DataFrame(articles)
    #text preprocessing
    text = preprocessing()
    keyword_list = keywords_of_article()
    list_keywords = keyword_list
    text_cleaner = pd.DataFrame({'text_cleaner':text, 'list_keywords':list_keywords})
    dataset = dataset.join(text_cleaner)
    return dataset

# get articles by keyword
def getarticles(keyword):
    #get of articles the collection  articles
    dataset = articles_of_mongoname_database()
    #Save list of articles in dataframe format
    dataset = pd.DataFrame(dataset)
    dataset = dataframe_articles()
    data = dataset[dataset['list_keywords'].apply(lambda x: any((i for i\
    in x if i.find(keyword) >= 0)))]
    return data[['_id', 'headline', 'author', 'text', 'url']]