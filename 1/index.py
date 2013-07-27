import tornado.wsgi
import logging

from crawler import CrawlerHandler, CrawlerCallbackHandler
 
import dao

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world! - Tornado\n")        

class ApiHandler(tornado.web.RequestHandler):
    def initialize(self):
        self._logger = logging.getLogger(__name__)

    def get(self):
        lat1 = self.get_argument("lat1", None)
        lng1 = self.get_argument("lng1", None)
        lat2 = self.get_argument("lat2", None)
        lng2 = self.get_argument("lng2", None)

        self._logger.info("(%s, %s) - (%s, %s)" % (lng1, lat1, lng2, lat2))

        def _func(db):
            criteria = None
            if lat1 is not None and lng1 is not None and lat2 is not None and lng2 is not None:
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

            self._logger.debug("Criteria %s" % repr(criteria))
            cursor = db.news.find(criteria)
        
            news_list = []            
            for doc in cursor:
                self._logger.debug("Found doc")
                # self._logger.info("Found doc %s" % repr(doc))
                news_list.append(doc)

            # self.write(news_list)

        dao.db_action(_func)


app = tornado.wsgi.WSGIApplication([
    (r"/", MainHandler),
    (r"/api", ApiHandler),
    (r"/crawler/callback", CrawlerCallbackHandler),
    (r"/crawler", CrawlerHandler)
])
 
from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)