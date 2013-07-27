import json

from bae.api import logging

import tornado.web

import dao

def _normalize_news(news):
    if news:
        if "like" not in news:
            news["like"] = 0
        if "dislike" not in news:
            news["dislike"] = 0
        news["id"] = news.pop("_id")

    return news

class ApiHandler(tornado.web.RequestHandler):
    def initialize(self):
        self._logger = logging.getLogger("api")

    def get(self):
        news_id = self.get_argument("id", None)

        lng1 = self.get_argument("lng1", None)
        lat1 = self.get_argument("lat1", None)
        lng2 = self.get_argument("lng2", None)
        lat2 = self.get_argument("lat2", None)

        if news_id:
            self._get_news_by_id(news_id)
        elif lng1 is not None and lat1 is not None and lng2 is not None and lat2 is not None:
            self._find_news_by_geo_range(lng1, lat1, lng2, lat2)

        else:
            self.write({
                "code": -1,
                "message": "Unknown request"
            })

    def post(self):
        news_id = self.get_argument("id", None)
        like = self.get_argument("like", None)

        if news_id and like:
            def _func(db):
                if like == "1":
                    update = {"$inc" : {"like":1}}
                else:
                    update = {"$inc" : {"dislike":1}}
                db.news.update({"_id":news_id}, update)
            dao.db_action(_func)
            self.write({"code":0})
        else:
            self.write({
                "code": -1,
                "message": "Missing argument 'id' or 'like'"
            })

    def _get_news_by_id(self, news_id):
        def _func(db):
            news = db.news.find_one({"_id":news_id})
            self.write(_normalize_news(news))

        dao.db_action(_func)

    def _find_news_by_geo_range(self, lng1, lat1, lng2, lat2):
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
                logging.debug("Found doc: %s" % type(doc.get("title")))
                news_list.append(_normalize_news(doc))

            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(json.dumps(news_list))

        dao.db_action(_func)