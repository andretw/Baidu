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
from loc_keywords import locations

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

def find_detail_loc(link, area):
    text = urllib.urlopen(link).read()

    logging.debug("Fetched %s" % link)
    # logging.debug(text)

    pattern = area.encode("gbk")
    match = re.search(pattern, text)

    if match:
        logging.debug(match.group(0))

    q = {
        "address": area.encode("utf-8")
    }

    map_api = "http://api.map.baidu.com/geocoder/v2/?output=json&ak=%s&%s" % (MAP_KEY, urlencode(q))
    response = urllib.urlopen(map_api).read()    
    logging.debug("Query %s" % map_api + ":" + response)

    addr = area
    location = None
    if response:
        response = json.loads(response)
        location = response.get("result").get("location")
        location = [ location.get("lng"), location.get("lat") ]

    return addr, location

def save_news(entries):
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

def crawl_news(area):
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
            addr, location = find_detail_loc(entry.link, area)

            entries.append({
                "_id": entry.link,
                "title": entry.title,
                "description": entry.description,
                "addr": addr,
                "loc": location
            })
        except:
            logging.exception("ERROR when crawl %s" % entry.link)

    save_news(entries)    

class CrawlerHandler(tornado.web.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        for loc in locations:
            crawl_news(loc)

if __name__ == "__main__":
    crawl_news(u"北京")
    crawl_news(u"河北")