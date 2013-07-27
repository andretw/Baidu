# -*- coding: utf-8 -*-

from bae.core import const
from bae.api import logging

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

def _find_location(link, area):
    text = unicode(urllib.urlopen(link).read(), 'gbk')

    logging.debug("Fetched %s, type %s" % (link, type(text)))
    # logging.debug(text)

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

def _crawl_news(area):
    logging.debug("crawler")
    logging.info("crawler")
    entries = []
    try:
        area_query = quote(area.encode('gbk'))
        rss_url = "http://news.baidu.com/ns?word="+ area_query +"%2B%CE%DB%C8%BE&tn=newsrss&sr=0&cl=2&rn=20&ct=0"
        logging.debug("rss_url: " + rss_url)
        ret = feedparser.parse(rss_url) 

        logging.debug("Found %d entries" % len(ret.entries))
    except:
        logging.exception('ERROR when reading rss')
        return

    for entry in ret.entries:
        try:
            addr, location = _find_location(entry.link, area)

            entries.append({
                "_id": entry.link,
                "title": entry.title,
                "description": entry.description,
                "addr": addr,
                "loc": location
            })
        except Exception:
            logging.exception("ERROR when crawl %s" % entry.link)

    _save_news(entries)    

class CrawlerHandler(tornado.web.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        for loc in locations:
            _crawl_news(loc)

if __name__ == "__main__":
    _crawl_news(u"北京")
    _crawl_news(u"河北")