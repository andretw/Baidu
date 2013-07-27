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
            self._crawl_news(loc)

    def _crawl_news(self, area):
        logging.debug("crawler")
        logging.info("crawler")
        entries = []
        try:
            area_query = quote(area.encode('gbk'))
            rss_url = "http://news.baidu.com/ns?word="+ area_query +"%2B%CE%DB%C8%BE&tn=newsrss&sr=0&cl=2&rn=20&ct=0"
            logging.debug("rss_url: " + rss_url)
            ret = feedparser.parse(rss_url) 

            logging.debug("Found %d entries" % len(ret.entries))
            self.write("Found %d entries for %s" % (len(ret.entries),area))
        except:
            logging.exception('ERROR when reading rss')
            return

        for entry in ret.entries:
            try:
                text = self._fetch_url(entry.link)
                if text:
                    addr, location = _find_location(text, area)

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

    def _fetch_url(self, url):
        self.write("Fetching %s" % url)
        # text = unicode(urllib.urlopen(url).read(), 'gbk')
        # logging.debug("Fetched %s" % url)
        # logging.debug(text)

        # tqmgr = BaeTaskQueueManager.getInstance()

        q = BaeTaskQueue("crawler_queue")

        ### 推入预执行的task
        qid = q.push(url = url)['response_params']['task_id']

        ### 查看task的执行信息
        # logging.debug("QUEUE: %s" + repr(q.getTaskInfo(qid)))

        ### 查看当前queue的信息
        # q.query()

        ### 查询用户所有的queue信息
        # tqmgr.getList()


class CrawlerCallbackHandler(tornado.web.RequestHandler):

    def get(self):
        logging.info("Crawler GET callback: %s" % self.request.query)

    def post(self):
        logging.info("Crawler POST callback: %s" % self.request.body)
        
        try:
            q = BaeTaskQueue("crawler_queue")
            task_id = self.get_argument("task_id")
            logging.debug("TaskInfo %s: %s" % (task_id, repr(q.getTaskInfo(task_id))))
        except Exception:
            logging.exception("callback error")

if __name__ == "__main__":
    _crawl_news(u"北京")
    _crawl_news(u"河北")