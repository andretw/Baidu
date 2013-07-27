# -*- coding: utf-8 -*-

from bae.core import const
from bae.api import logging
from bae.api.taskqueue import BaeTaskQueueManager
from bae.api.taskqueue import BaeTaskQueue

import re
import json
import urllib
from urllib import quote, urlencode

import tornado.web
import pymongo

import feedparser
from loc import locations

MAP_KEY = "AD07295d48aebd5c11b10c539cd1090b"

BAIDU_SEARCH_URL = "http://www.baidu.com/baidu"

def _build_geo_index():
    con = None
    try:
        db_name = 'ZwgmbiQSlqOsjZWOKIOJ'
        con = pymongo.Connection(host = const.MONGO_HOST, port = int(const.MONGO_PORT))
        db = con[db_name]
        db.news.create_index([("loc", pymongo.GEO2D)])
    except:
        logging.exception('ERROR fail to create geo index')
    finally:
        if con:
            con.disconnect()

# _build_geo_index()

def _find_location(text, area):
    addr = area    
    for sub in locations[area]:
        match = re.search(sub, text)
        if match:
            addr = addr + sub
            break

    logging.debug("addr -> %s" % addr)

    q = {"address": addr.encode("utf-8")}
    map_api = "http://api.map.baidu.com/geocoder/v2/?output=json&ak=%s&%s" % (MAP_KEY, urlencode(q))
    response = urllib.urlopen(map_api).read()    

    location = None
    if response:
        response = json.loads(response)
        location = response.get("result").get("location")
        location = [ location.get("lng"), location.get("lat") ]

    return addr, location

def _save_news(entries):
    if not entries:
        return
    try:
        db_name = 'ZwgmbiQSlqOsjZWOKIOJ'
        con = pymongo.Connection(host = const.MONGO_HOST, port = int(const.MONGO_PORT))
        db = con[db_name]

        if const.MONGO_USER:
            db.authenticate(const.MONGO_USER, const.MONGO_PASS)
        news = db.news

        news.insert(entries)

        logging.debug("Saved %d documents" % len(entries))
    except:
        logging.exception('ERROR when save into mongodb')
    finally:
        if con:
            con.disconnect()

  class CrawlerHandler(tornado.web.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        for loc in [ u"北京", u"河北" ]:
            _crawl_news(loc, self)

class CrawlerCallbackHandler(tornado.web.RequestHandler):

    def get(self):
        logging.info("Crawler GET callback: %s" % self.request.query)

    def post(self):
        logging.info("Crawler POST callback: %s" % self.request.body)

if __name__ == "__main__":
    _crawl_news(u"北京")
    _crawl_news(u"河北")