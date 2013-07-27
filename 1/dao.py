from bae.core import const
from bae.api import logging

import pymongo

def build_geo_index():
    def _func(db):
        db.news.create_index([("loc", pymongo.GEO2D)])
    db_action(_func)

def db_action(func):
    try:
        db_name = 'ZwgmbiQSlqOsjZWOKIOJ'
        con = pymongo.Connection(host = const.MONGO_HOST, port = int(const.MONGO_PORT))
        db = con[db_name]

        if const.MONGO_USER:
            db.authenticate(const.MONGO_USER, const.MONGO_PASS)

        return func(db)
    except:
        logging.exception('ERROR in dao')
    finally:
        if con:
            con.disconnect()
            
build_geo_index()