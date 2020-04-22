import scrapy
from CrawlerTheguardian.items import ArticleItem




class spiders(scrapy.Spider):
    name="CrawlerTheguardian"
    #categorie=['world','lifeandstyle','commentisfree','sport','culture','lifeandstyle']
    start_urls = ['https://www.theguardian.com/commentisfree/all']

    def parse(self, response):
        ARTICLE_URL_SELECTOR = '//*[contains(@class,"fc-item__link")]//@href'
        for article_url in response.xpath(ARTICLE_URL_SELECTOR).extract():
            yield scrapy.Request(
                url=article_url,
                callback=self.parsearticle
            )

        NEXT_PAGE_SELECTOR = '//*[contains(@class,"pagination__action--static") and contains(@rel,"next")]//@href'
        next_page = response.xpath(NEXT_PAGE_SELECTOR).extract_first()
        if(next_page):
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )

    def parsearticle(self, response):
        # Test if the article is already crawled
        if('cached' in response.flags):
            return

        HEADLINE_SELECTOR = '//*[contains(@itemprop,"headline")]//text()'
        TEXT_SELECTOR = '//*[contains(@class,"content__article-body")]//p//text()'
        AUTHOR_SELECTOR = '//*[contains(@rel,"author")]//*/text()'
        
        
        item = ArticleItem()
        
        item['author'] = response.xpath(AUTHOR_SELECTOR).extract()
        item['headline']= response.xpath(HEADLINE_SELECTOR).extract_first()
        item['text' ]= ''.join(response.xpath(TEXT_SELECTOR).extract())
        item['url']=  response.request.url
        
        yield item