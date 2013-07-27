# -*- coding: utf-8 -*-

from bae.core import const
from bae.api import logging
from bae.api.taskqueue import BaeTaskQueue

import re
import json
import urllib
from urllib import quote, urlencode

import tornado.web
import pymongo

import feedparser
from loc import locations
import dao

MAP_KEY = "AD07295d48aebd5c11b10c539cd1090b"

BAIDU_SEARCH_URL = "http://www.baidu.com/baidu"

def _find_location(text, area):
    addr = area    
    for sub in locations[area]:
        match = re.search(sub, text)
        if match:
            addr = addr + sub
            break

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
    def initialize(self):
        self._logger = logging.getLogger("crawler")

    def get(self):
        self.post()

    def post(self):
        for area in [ u"北京", u"河北" ]:
            self._crawl_news(area)

    def _crawl_news(self, area):
        try:
            area_query = quote(area.encode('gbk'))
            rss_url = "http://news.baidu.com/ns?word="+ area_query +"%2B%CE%DB%C8%BE&tn=newsrss&sr=0&cl=2&rn=20&ct=0"
            self._logger.debug("rss_url: " + rss_url)
            ret = feedparser.parse(rss_url) 

            self._logger.debug("Found %d entries" % len(ret.entries))
            self.write("Found %d entries for %s" % (len(ret.entries),area))

            self._save_news(area, ret.entries)   
        except:
            self._logger.exception('ERROR when reading rss')
            return

        for entry in ret.entries:
            try:
                self._fetch_url(entry.link)
            except Exception:
                self._logger.exception("ERROR when crawl %s" % entry.link)

    def _save_news(self, area, entries):
        if not entries:
            return

        saved_news = []
        for entry in entries:
            saved_news.append({
                "_id": entry.link,
                "title": entry.title,
                "description": entry.description,
                "area": area
            })

        def _save_entries(db):
            db.news.insert(saved_news)
            self._logger.debug("Saved %d documents" % len(saved_news))
            self.write("Saved %d documents" % len(saved_news))

        dao.db_action(_save_entries)

    def _fetch_url(self, url):
        q = BaeTaskQueue("crawler_queue")
        q.push(url = url, callback_url = "http://ecomap.duapp.com/crawler/callback")
        self.write("Queue fetch task: "+url)

class CrawlerCallbackHandler(tornado.web.RequestHandler):

    def initialize(self):
        self._logger = logging.getLogger("crawler_callback")

    def get(self):
        self._logger.info("Crawler GET callback: %s" % self.request.query)

    def post(self):
        try:
            task_id = int(self.get_argument("task_id"))
            self._logger.info("Crawler POST callback: %s" % task_id)

            q = BaeTaskQueue("crawler_queue")
            task_info = q.getTaskInfo(task_id)
            response_params = task_info["response_params"]
            text = response_params.pop("result_data")
            self._logger.debug("response_params[%s] = %s" % (task_id, repr(response_params)))
            task_desc = response_params["task_desc"]
            task_desc = json.loads(task_desc)
            url = task_desc["url"]

            def _get_doc(db):
                return db.news.find_one({"_id":url})

            doc = dao.db_action(_get_doc)

            if doc:
                area = doc.get("area")

                addr, location = _find_location(text, area)
                self._logger.debug("Found addr %s in %s" % (addr, url))

                def _update_doc(db):
                    db.update({"_id":url}, {"$set":{"addr":addr, "loc":location}})
                    self._logger.info("Update %s with addr %s, loc %s" % (url, addr, location))
                dao.db_action(_update_doc)
            else:
                self._logger.error("Cannot found url "+url)

        except Exception:
            self._logger.exception("callback error")

if __name__ == "__main__":
    _crawl_news(u"北京")
    _crawl_news(u"河北")