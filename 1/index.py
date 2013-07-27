import tornado.wsgi
from bae.api import logging

from crawler import CrawlerHandler, CrawlerCallbackHandler
 
import dao

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world! - Tornado\n")        

class ApiHandler(tornado.web.RequestHandler):
    def initialize(self):
        self._logger = logging.getLogger("api")

    def get(self):
        lat1 = self.get_argument("lat1", None)
        lng1 = self.get_argument("lng1", None)
        lat2 = self.get_argument("lat2", None)
        lng2 = self.get_argument("lng2", None)

        self.write("lat1="+lat1)
        self.write("lng1="+lng1)
        self.write("lat2="+lat2)
        self.write("lng2="+lng2)
        
        def _func(db):
            criteria = None
            # if lat1 is not None and lng1 is not None and lat2 is not None and lng2 is not None:
            criteria = {
                    "loc": {
                        "$within": {
                            "$box":[
                                [float(lng1), float(lat1)], 
                                [float(lng2), float(lat2)]
                            ]
                        }
                    }
                }

            cursor = db.news.find(criteria)
        
            news_list = []            
            for doc in cursor:
                self._logger.debug("Found doc")
                # self._logger.info("Found doc %s" % repr(doc))
                news_list.append(doc)

            self.write(news_list)

        dao.db_action(_func)


app = tornado.wsgi.WSGIApplication([
    (r"/", MainHandler),
    (r"/api", ApiHandler),
    (r"/crawler/callback", CrawlerCallbackHandler),
    (r"/crawler", CrawlerHandler)
])
 
from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)