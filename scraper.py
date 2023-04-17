from time import sleep
from bs4 import BeautifulSoup
from requests import get
from scrapy import Spider, crawler
from gpt import Embeddings
from database import Db
from config import config, is_allowed, is_skipped

class Page():
    def __init__(self, url):
        self.page = get(url).text
        self.sections = []
        soup = BeautifulSoup(self.page, "html.parser")
        start = soup.find("p")
        try:
            self.sections.append(start.get_text())
        except AttributeError:
            return
        self.add_section(start)
    
    def add_section(self, start):    
        curr_section = ""
        for elem in start.next_siblings:
            if elem.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                curr_soup = BeautifulSoup(curr_section, features="lxml")
                self.sections.append(curr_soup.getText())
                curr_section = ""
            else:
                curr_section += elem.__str__()

class SiteSpider(Spider):
    name = "all"
    linkss = []
    #custom_settings = {"LOG_LEVEL": "INFO"}
    
    def __init__(self, embeddingsApi, db, is_allowed, is_skipped):
        self.embeddings = embeddingsApi
        self.db = db
        self.is_allowed = is_allowed
        self.is_skipped = is_skipped

    def parse(self, response):
        print(response.url)
        if response.url not in SiteSpider.linkss and self.is_allowed(response.url) and not self.is_skipped(response.url):
            SiteSpider.linkss.append(response.url)
            
            page = Page(response.url)
            print("Adding " + response.url)
            
            
            for section in page.sections:
                sleep(1) # because of openai rate limiting
                embedding_data = self.embeddings.create(section)
                if "data" not in embedding_data.keys():
                    print(embedding_data["error"]["message"])
                    raise Exception(embedding_data["error"]["message"])
                self.db.add_embeddings(embedding_data, text=section)
            
            
            for href in response.css("a::attr(href)"):
                yield response.follow(href, self.parse)
                
            
def scrape(embeddings, db):
    SiteSpider.start_urls = config["start_urls"]
    SiteSpider.allowed_domains = config["allowed_domains"]
    process = crawler.CrawlerProcess({"USER_AGENT": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"})
    process.crawl(
        SiteSpider, 
        embeddingsApi=Embeddings(), 
        db=Db(),
        is_allowed=is_allowed,
        is_skipped=is_skipped
    )
    process.start()