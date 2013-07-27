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

        def _func(db):
            criteria = None
            if lat1 is not None and lng1 is not None and lat2 is not None and lng2 is not None:
                criteria = {"$within":{"$box":[[float(lng1), float(lat1)], [float(lng2), float(lat2)]]}}

            news_list = db.news.find(criteria)

            self._logger.debug("Found news %d" % len(news_list))

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