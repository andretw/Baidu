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

def _find_location(text, area, _logger):
    addr = area    
    for sub in locations[area]:
        match = re.search(unicode(sub,"gbk"), text)
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

def _crawl_news(area, _logger):
    try:
        area_query = quote(area.encode('gbk'))
        rss_url = "http://news.baidu.com/ns?word="+ area_query +"%2B%CE%DB%C8%BE&tn=newsrss&sr=0&cl=2&rn=20&ct=0"
        _logger.debug("rss_url: " + rss_url)
        ret = feedparser.parse(rss_url) 

        _logger.debug("Found %d entries" % len(ret.entries))

        _save_news(area, ret.entries, _logger)   
    except:
        _logger.exception('ERROR when reading rss')
        return

    for entry in ret.entries:
        try:
            _fetch_url(entry.link)
        except Exception:
            _logger.exception("ERROR when crawl %s" % entry.link)

def _save_news(area, entries, _logger):
    if not entries:
        return

    saved_news = []
    for entry in entries:
        news = {
            "_id": entry.link,
            "title": entry.title,
            "description": entry.description,
            "area": area
        }
        saved_news.append(news)

        def _save_entries(db):
            db.news.insert(news)
            _logger.debug("Saved %s" % entry.link)
        dao.db_action(_save_entries)

    # def _save_entries(db):
    #     db.news.insert(saved_news)
    #     _logger.debug("Saved %d documents %s" % (len(saved_news), repr(saved_news)))

    # dao.db_action(_save_entries)

def _fetch_url(url):
    q = BaeTaskQueue("crawler_queue")
    q.push(url = url, callback_url = "http://ecomap.duapp.com/crawler/callback")

class CrawlerHandler(tornado.web.RequestHandler):
    def initialize(self):
        self._logger = logging.getLogger("crawler")

    def get(self):
        self.post()

    def post(self):
        url = self.get_argument("url", None)
        area = self.get_argument("area", None)
        if url:
            _fetch_url(url)
        elif area:
            _crawl_news(area, self._logger)
        else:
            for area in [ u"北京", u"河北" ]:
                _crawl_news(area, self._logger)

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

                try:
                    addr, location = _find_location(text, area, self._logger)
                    # self._logger.debug("Found addr %s in %s" % (addr, url))

                    def _update_doc(db):
                        db.news.update({"_id":url}, {"$set":{"addr":addr, "loc":location}})
                        # self._logger.info("Update %s with addr %s, loc %s" % (url, addr, location))
                    dao.db_action(_update_doc)
                except Exception:
                    self._logger.exception("Fail to analyze address for "+url)
            else:
                self._logger.error("Cannot found doc for url "+url)

        except Exception:
            self._logger.exception("callback error")

if __name__ == "__main__":
    text = urllib.urlopen("http://www.chinanews.com/df/2013/07-25/5084700.shtml").read()
    addr, location = _find_location(text, u"河北")
    print addr
