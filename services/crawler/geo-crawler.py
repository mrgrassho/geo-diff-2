#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import aiohttp
import argparse
from os import mkdir, environ
from os.path import join, exists, isfile, dirname
from time import time, sleep
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

dotenv_path = join(dirname(__file__), '.env')
try:
    load_dotenv(dotenv_path)
except expression as e:
    raise Exception(f" {bcolors.FAIL}[-]{bcolors.ENDC} Can't locate .env file") 

BASE_URL = environ.get("BASE_URL")
PRODUCT = environ.get("PRODUCT")
TILE_MATRIX_SET = environ.get("TILE_MATRIX_SET")
FILE_FORMAT = environ.get("FILE_FORMAT")
DIR_TILES = environ.get("DIR_TILES")


class bcolors:
   HEADER = '\033[95m'
   OKBLUE = '\033[94m'
   OKGREEN = '\033[92m'
   WARNING = '\033[93m'
   FAIL = '\033[91m'
   ENDC = '\033[0m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'


class GeoCrawler(object):
    
    def __init__(self, fdates, out_dir=DIR_TILES, fbound=None, zoom_level_end=6, concurrency_level=20, timeout=40, verbose=False, coord_img_only=False):
        if (not exists(fdates)):
            raise Exception(f" {bcolors.FAIL}[-]{bcolors.ENDC} File '{fdates}' not found.")
        with open(fdates, 'r') as f:
            self.dates = [ s.split("\n")[0] for s in f.readlines()]
        
        self.out_dir = join(out_dir, "RAW")
        if (not exists(out_dir)):
            mkdir(out_dir)
        if (not exists(self.out_dir)):
            mkdir(self.out_dir)
        if (fbound is not None):
            with open(fbound, 'r') as f:
                self.boundaries = [ s.split("\n")[0] for s in f.readlines()]
        else:
            self.boundaries = []
        self.verbose = verbose
        if (zoom_level_end > 10):
            zoom_level_end = 10
        elif (zoom_level_end < 2):
            zoom_level_end = 2
        self.zoom_level = [ i for i in range(2, zoom_level_end+1)]
        self.concurrency_level = concurrency_level
        self.timeout = timeout
        self.coord_img_only = coord_img_only
        

    async def fetch(self, session, url):
        try:
            async with session.get(url) as response:
                data = None
                purl = url[99:]
                if (response.status >= 200 and response.status < 300):
                    data = await response.read()
                    print(f" {bcolors.OKGREEN}[+]{bcolors.ENDC} {purl}{bcolors.OKGREEN} ({response.status} {response.reason}) {bcolors.ENDC}") if (self.verbose) else ''
                elif (response.status >= 300 and response.status < 400):
                    print(f" {bcolors.WARNING}[!]{bcolors.ENDC} {purl}{bcolors.WARNING} ({response.status} {response.reason}) {bcolors.ENDC}") if (self.verbose) else ''
                elif (response.status >= 400):
                    print(f" {bcolors.FAIL}[-]{bcolors.ENDC} {purl}{bcolors.FAIL} ({response.status} {response.reason}) {bcolors.ENDC}") if (self.verbose) else ''
                return data
        except Exception as e:
            if (self.verbose):
                print(f" {bcolors.FAIL}[!] Could not download {url} – ERROR: {e} {bcolors.ENDC}")
            return None


    async def save(self, fpath, data):
        with open(fpath, 'wb') as f:
            f.write(data)


    async def download(self, fpath, url):
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            page = await self.fetch(session, url)
            if (page is None):
                return None
            await self.save(fpath,page)


    def resources(self, date):
        listyx = lambda n: range(2**n)
        res = []
        prev_path = join(self.out_dir, date)
        if (not exists(prev_path)):
            mkdir(prev_path)
        for z in self.zoom_level:
            prev_path = join(self.out_dir, date, f"{z}")
            if (not exists(prev_path)):
                mkdir(prev_path)
            for y in listyx(z):
                for x in listyx(z):
                    zyx = f"{z},{y},{x}"
                    if (z > 5 and zyx in self.boundaries) or (z <= 5):
                        prev_path = join(self.out_dir, date, f"{z}", f"{y}")
                        if (not exists(prev_path)):
                            mkdir(prev_path)
                        url = f"{BASE_URL}/{PRODUCT}/default/{date}/{TILE_MATRIX_SET}/{z}/{y}/{x}.{FILE_FORMAT}"
                        fpath = join(self.out_dir, date, f"{z}", f"{y}", f"{x}")
                        # Avoid duplicates
                        if (not exists(fpath)):
                            res.append((fpath, url))                        
                        if (self.coord_img_only):
                            self.coord_img(z, y, x, fpath)
        return res


    def process(self):
        for date in self.dates:
            resources = self.resources(date)
            if (not self.coord_img_only):
                while len(resources) != 0:
                    loop = asyncio.get_event_loop()
                    f = asyncio.wait([self.download(*res) for res in resources[:self.concurrency_level]])
                    loop.run_until_complete(f)
                    resources = resources[self.concurrency_level:]

    
    def coord_img(self, z, y, x, fpath):
        image_width = 256
        image_height = 256
        img = Image.new('RGB', (image_width, image_height), color=(51, 144, 255))
        # create the canvas
        canvas = ImageDraw.Draw(img)
        font = ImageFont.truetype('Arial.ttf', size=24)
        text_width, text_height = canvas.textsize('Hello World', font=font)
        x_pos = int((image_width - text_width) / 2)
        y_pos = int((image_height - text_height) / 2)
        canvas.text((x_pos, y_pos), f"z={z},y={y},x={x}", font=font, fill='#FFFFFF')
        img.save(fpath, format='JPEG')


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('fdates', type=str, help="Specify file with dates to process")
    parser.add_argument('-o', '--out_dir', type=str, default=DIR_TILES, help="Specify output directory")
    parser.add_argument('-b', '--boundaries', type=str, default=None, help="Specify file with boundaries")
    parser.add_argument('-c', '--concurrency', type=int, default=20, help="Specify number of concurrent HTTP requests")
    parser.add_argument('-t', '--timeout', type=int, default=20, help="Specify HTTP Timeout (in seconds)")
    parser.add_argument('-z', '--zoom-level-end', type=int, default=7, help="Specify max zoom. It starts at level 2 and finalizes at specified level")
    parser.add_argument('-nv', '--not-verbose', action='store_false', default=True, help="Show no messages during process")
    parser.add_argument('-ci', '--coord-img-only', action='store_true', default=False, help="Generate just images with the coord, useful to select certain part of the map instead of downloading everything")
    args = parser.parse_args()
    c = GeoCrawler(args.fdates, out_dir=args.out_dir, fbound=args.boundaries, zoom_level_end=args.zoom_level_end, concurrency_level=args.concurrency, timeout=args.timeout, verbose=args.not_verbose, coord_img_only=args.coord_img_only)
    c.process()

if __name__ == '__main__':
    main()
