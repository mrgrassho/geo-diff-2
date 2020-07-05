#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import listdir, environ
from os.path import join, dirname, isfile
from pymongo import MongoClient
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
client = MongoClient(environ.get("MONGO_URI"))
DIR_TILES = environ.get("DIR_TILES")

def get_index():
    index = []
    filters = listdir(DIR_TILES)
    for f in filters:
        dates = listdir(join(DIR_TILES,f))
        for date in dates:
            if not isfile(join(DIR_TILES,f,date)):
                index.append({
                    'filterName': f,
                    'date': date
                })
    return index

def update():
    db = client['geo-mongo']
    db.geo_index.drop()
    db.geo_index.insert_many(get_index())

def main():
    update()

if __name__ == '__main__':
    main()