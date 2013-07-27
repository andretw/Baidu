import json

from bae.api import logging

import tornado.web

import dao

class ApiHandler(tornado.web.RequestHandler):
    def initialize(self):
        self._logger = logging.getLogger("api")

    def get(self):
        lat1 = self.get_argument("lat1", None)
        lng1 = self.get_argument("lng1", None)
        lat2 = self.get_argument("lat2", None)
        lng2 = self.get_argument("lng2", None)
        
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
                self._logger.debug("Found doc: %s" % type(doc.get("title")))
                # self._logger.info("Found doc %s" % repr(doc))
                news_list.append(doc)

            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(json.dumps(news_list))

        dao.db_action(_func)