#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pika import SelectConnection, URLParameters
from dotenv import load_dotenv
from os import walk, environ
from os.path import join, dirname
from pathlib import Path
from time import sleep, time
from json import dumps, loads
from base64 import b64encode, b64decode
from functools import partial

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Updater(object):
    def __init__(self, debug=True, prefetch_count=1):
        self._path = environ['DIR_TILES']
        self._wait = int(environ['WAIT'])
        self._debug = debug
        self._res_queue = environ['RES_QUEUE']
        self._res_xchg = environ['RES_XCHG']
        self._amqp_url = environ['AMPQ_URL']
        self._prefetch_count = prefetch_count
        self._reconection_time = int(environ['TIMEOUT'])


    def base64_to_img(self, buff, fpath):
        with open(fpath, 'wb') as f:
            b64data = buff.split(",")[1]
            data = b64decode(b64data.encode("utf-8", "ignore"))
            f.write(data)


    def callback_res_queue(self, _unused_channel, delivery, properties, body):
        """
        Callback triggered when message is received.
        """
        if (self._debug):
            print(" [x] Received - Body: {}".format(body[:140]))
        start_time = time()
        data = loads(body)
        path = data['earthImage']['path']
        if ('filteredImages' in data):
            if (self._debug):
                print(" [x] Saving Images...")
            for image in data['filteredImages']:
                new_path = Path(path.replace('RAW', image['filterName']))
                dirs = new_path.parts[:-1]
                # create dirs
                Path("/".join(dirs)).mkdir(parents=True, exist_ok=True)
                self.base64_to_img(image['vectorImage'], new_path)
        self._channel.basic_ack(delivery_tag=delivery.delivery_tag)


    def on_open_connection(self, _unused_frame):
        if (self._debug):
            print(" [x] Connected - Connection state: OPEN. ")
        self._connection.channel(on_open_callback=self.on_channel_open)


    def on_channel_open(self, channel):
        """Callback when we have successfully declared the channel."""
        if (self._debug):
            print(" [x] Channel - Channel state: OPEN. ")
        self._channel = channel
        self._channel.exchange_declare(exchange=self._res_xchg, exchange_type='fanout')
        cb = partial(self.on_queue_declareok, userdata=self._res_queue)
        self._channel.queue_declare(queue=self._res_queue, durable=True, callback=cb)


    def on_queue_declareok(self, _unused_frame, userdata):
        """Callback when we have successfully declared the queue.

        This call tells the server to send us self._prefetch_count message in advance.
        This helps overall throughput, but it does require us to deal with the messages
        we have promptly.
        """
        queue_name = userdata
        if (self._debug):
            print(" [x] Queue declared - Queue: {}".format(queue_name))
        self._channel.basic_qos(prefetch_count=self._prefetch_count, callback=self.on_qos)
        self._channel.queue_bind(exchange=self._res_xchg, queue=queue_name)


    def on_qos(self, _unused_frame):
        """Callback when Basic.QOS has completed."""
        if (self._debug):
            print(" [x] QOS set to {}".format(self._prefetch_count))
        self.start_consuming()


    def start_consuming(self):
        """Start consuming from task queue."""
        if (self._debug):
            print(" [x] Waiting for messages...")
        self._channel.basic_consume(self._res_queue, self.callback_res_queue)


    def start(self):
        """Start worker."""
        # Define connection
        while True:
            try:
                self._connection = SelectConnection(URLParameters(self._amqp_url), on_open_callback=self.on_open_connection)
                self._connection.ioloop.start()
            # Catch a Keyboard Interrupt to make sure that the connection is closed cleanly
            except KeyboardInterrupt:
                # Gracefully close the connection
                self._connection.close()
                # Start the IOLoop again so Pika can communicate, it will stop on its own when the connection is closed
                self._connection.ioloop.start()
            except :
                if (self._debug):
                    print(" [!] RabbitMQ Host Unrecheable. Reconecting in {} seconds...".format(self._reconection_time))
                sleep(self._reconection_time)


u = Updater()
u.start()