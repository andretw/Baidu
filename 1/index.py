import tornado.wsgi

from crawler import CrawlerHandler, CrawlerCallbackHandler
 
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world! - Tornado\n")        

 
app = tornado.wsgi.WSGIApplication([
    (r"/", MainHandler),
    (r"/crawler/callback", CrawlerCallbackHandler),
    (r"/crawler", CrawlerHandler)
])
 
from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)