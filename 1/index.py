import tornado.wsgi
 
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world! - Tornado\n")        
 
app = tornado.wsgi.WSGIApplication([
    (r"/", MainHandler),
])
 
from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)