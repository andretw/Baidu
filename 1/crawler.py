import tornado.web
import feedparser

from bae.core import const
import pymongo

BAIDU_SEARCH_URL = "http://www.baidu.com/baidu"

def crawl_news():
    ret = feedparser.parse("http://news.baidu.com/ns?word=%CE%DB%C8%BE&tn=newsrss&sr=0&cl=2&rn=20&ct=0") 

    db_name = 'ecomap'
    con = pymongo.Connection(host = const.MONGO_HOST, port = int(const.MONGO_PORT))
    db = con[db_name]
    db.authenticate(const.MONGO_USER, const.MONGO_PASS)
    news = db.news

    try:
        # print ret.feed    
        for entry in ret.entries:
            print 20*"-"
            print entry.title
            print entry.link
            print entry.description

            news.insert({
                "title": entry.title,
                "link": entry.link,
                "description": entry.description
            })
    finally:
        con.disconnect()

class CrawlerHandler(tornado.web.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        crawl_news()

if __name__ == "__main__":
    crawl_news()