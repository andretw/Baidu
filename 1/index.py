import tornado.wsgi

from crawler import CrawlerHandler
 
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world! - Tornado\n")        
        
 
app = tornado.wsgi.WSGIApplication([
    (r"/", MainHandler),
    (r"/crawler", CrawlerHandler)
])
 
from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)