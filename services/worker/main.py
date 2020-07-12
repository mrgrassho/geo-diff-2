#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from geodiff_worker import GeoDiffWorker
from os import environ
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def main():
    """Main entry point to the program."""

    # Get the location of the AMQP broker (RabbitMQ server) from
    # an environment variable
    amqp_url = environ['AMQP_URL']
    task_queue = environ['TASK_QUEUE']
    result_xchg = environ['RES_XCHG']
    keep_alive_queue = environ['KEEP_ALIVE_QUEUE']
    worker = GeoDiffWorker(amqp_url, task_queue, result_xchg, keep_alive_queue, debug=True)
    worker.start()


if __name__ == '__main__':
    main()
