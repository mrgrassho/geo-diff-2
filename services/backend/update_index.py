#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import listdir, environ
from os.path import join, dirname, isfile
from pymongo import MongoClient
from dotenv import load_dotenv
from time import sleep

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
client = MongoClient(environ.get("MONGO_URI"))
DIR_TILES = environ.get("DIR_TILES")
UPDATE_WAIT = int(environ.get("UPDATE_WAIT"))

def remove_ds_store(ls):
    return [ f for f in ls if not f.endswith('.DS_Store')]

def get_index():
    index = []
    filters = listdir(DIR_TILES)
    filters = remove_ds_store(filters)
    all_filters = {}
    for f in filters:
        dates = listdir(join(DIR_TILES,f))
        dates = remove_ds_store(dates)
        for date in dates:
            if not isfile(join(DIR_TILES,f,date)):
                index.append({
                    'filterName': f,
                    'date': date
                })
                if (date not in all_filters):
                    all_filters[date] = 0
                else:
                    all_filters[date] += 1
    dates_all_filters = [key for (key,value) in all_filters.items() if value >= len(filters)]
    for date in dates_all_filters: 
        index.append({
            'filterName': 'ALL',
            'date': date
        })
    return index

def update():
    db = client['geo-mongo']
    db.geo_index.drop()
    db.geo_index.insert_many(get_index())

def main():
    while True:
        update()
        sleep(UPDATE_WAIT)

if __name__ == '__main__':
    main()