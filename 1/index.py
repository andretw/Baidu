import tornado.wsgi
from tornado.web import StaticFileHandler, RedirectHandler
from bae.core import const

from crawler import CrawlerHandler, CrawlerCallbackHandler
from api import ApiHandler

app = tornado.wsgi.WSGIApplication([
    (r"/api", ApiHandler),
    (r"/crawler/callback", CrawlerCallbackHandler),
    (r"/crawler", CrawlerHandler),
    (r"/", RedirectHandler, {"url": "/index.html"}),
    (r"^/(.*)$", StaticFileHandler, {"path": const.APP_DIR+"/static" })
])
 
from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)