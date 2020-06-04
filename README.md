### DataEngineeringCodingChallenge

The goal of this coding challenge is to create a solution that crawls for articles from a news website www.theguardian.com, cleanses the response, stores it in a mongo database, then makes it available to search via an API.


### Scrapy Theguardian
This crawler will crawl articles on a news website such as [theguardian.com](http://theguardian.com)  using a crawler framework such as [Scrapy](http://scrapy.org).

Theguardian spider crawls the following data:

key | type | description 
 --- | --- | --- 
author | Array of strings | Author(s) of the article.
headline | String | Headline of the article.
text | content | The article's content.
url | String | The article's page url.

While Crawler theguardian Pipelines simply stores article data in Mongodb's "articles" collection.
to execute the scrapy,run the command :
scrapy crawl CrawlerTheguardian

### modproject.py
this module allows the pre-proccessing of text of articles (remove figure, punctuation, and)
in addition it returns the keywords of each article text so that the user searches by the keyword

### api_Theguardian.ipynb
 API that provides access to the content in the mongo database. The user should be able to search for articles by keyword
 
 ### Note: this project is to be implemented under IDE netbeans
