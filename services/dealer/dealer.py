#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pika import BlockingConnection, URLParameters, BasicProperties
from dotenv import load_dotenv
from os import walk, environ
from os.path import join, dirname
from time import sleep
from json import dumps
from base64 import b64encode


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Dealer(object):
    def __init__(self, debug=True):
        self._path = environ['DIR_TILES']
        self._wait = int(environ['WAIT'])
        self._debug = debug
        self._task_queue = environ['TASK_QUEUE']
        self._amqp_url = environ['AMPQ_URL']


    def send_to_queue(self, message, queue):
        """
        Send message to RabbitMQ Queue.
        """
        json_msg = dumps(message)
        self._channel.queue_declare(queue=queue, durable=True)
        self._channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=json_msg,
            properties=BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )
        if (self._debug):
            print(" [x] Image sent to {} - Body: {} ".format(queue, json_msg[:10]))

    
    def img_to_base64(self, fpath):
        with open(fpath, 'rb') as f:
            return "data:image/png;base64," + b64encode(f.read()).decode("utf-8", "ignore") 


    def prepare(self, data, path):
        return {
            "earthImage" : {
                "rawImage": data,
                "url": '',
                "path": path
            }
        }


    def process(self, files):
        self._connection = BlockingConnection(URLParameters(self._amqp_url))
        self._channel = self._connection.channel()
        for f in files:
            data = self.img_to_base64(f)
            message = self.prepare(data, f)
            self.send_to_queue(message, self._task_queue)
            sleep(self._wait)
        self._connection.close()


    def watch(self):
        before = []
        while True:  
            after = [ join(p,f) for p, _, files in walk(self._path) for f in files if f != '.DS_Store']
            added = [f for f in after if f not in before]
            removed = [f for f in before if f not in after]
            if added: 
                # Limit zoom 2-5
                added = [ a for a in added if int(a.split('/')[5]) in (2,3,4,5)]
                self.process(added)
                print(f" [+] Added: {len(added)}")
            before = after
            sleep(self._wait)


d = Dealer()
d.watch()