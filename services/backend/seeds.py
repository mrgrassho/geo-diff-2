#!/usr/bin/env python3
# -*- coding": utf-8 -*-

from os import listdir, environ
from os.path import join, dirname, isfile
from pymongo import MongoClient
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
client = MongoClient(environ.get("MONGO_URI"))
DIR_TILES = environ.get("DIR_TILES")

new_filters = [
    { "_id": 1, "name": 'RAW', "longName": 'Raw Image', "active": True },
    { "_id": 2, "name": 'DESERT', "longName": 'Desert filtered Image', "active": True },
    { "_id": 3, "name": 'FOREST-JUNGLE', "longName": 'Forest/Jungle filtered Image', "active": True },
    { "_id": 4, "name": 'OCEAN-SEA', "longName": 'Ocean/Sea filtered Image', "active": True }
]

new_users = [
    { "_id": 1, "name": 'admin', "api_token": 'eyJhbGciOiJIUzM4NCJ9MTIzNAAZXCir'}
]

def seed():
    db = client['geo-mongo']
    filters = db['filters']
    filters.insert_many(new_filters)
    users = db['users']
    users.insert_many(new_users)

def main():
    seed()

if __name__ == '__main__':
    main()