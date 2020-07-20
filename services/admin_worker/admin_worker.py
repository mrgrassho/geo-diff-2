#!/usr/bin/env python
# -*- enconding: utf-8 -*-

from docker_client import DockerAPIClient
from pika import BlockingConnection, URLParameters
from pika.exceptions import AMQPConnectionError
from time import sleep
from threading import Thread
from functools import partial
from os import environ
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class BColors:
    GREY = '\u001b[37;1m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = "\u001b[0m"


class AdminWorker(object):

    def __init__(self, reconection_time=10, prefetch_count=1, debug=True):
        self._amqp_url = environ['AMQP_URL']
        self._task_queue = environ['TASK_QUEUE']
        self._reconection_time = int(environ['AMQP_TIMEOUT']) # 10 seconds
        self._last_timestamps = dict()
        self._lights = { # Is COLOR if less than assigned percentage
            'GREY': float(environ['GREY_LIGHT']), # Means IDLE
            'GREEN': float(environ['GREEN_LIGHT']),
            'YELLOW': float(environ['YELLOW_LIGHT']),
            'RED': float(environ['RED_LIGHT'])
        }
        self._prefetch_count = prefetch_count
        self._qty_task = int(environ['QTY_TASK'])
        self._max_scale = int(environ['MAX_SCALE'])
        self._min_scale = 1
        self._connection = None
        self._channel = None
        self._task_queue_obj = None
        self._service_monitor = environ['SERVICE_MONITOR']
        self._debug = debug


    def callback_task_queue(self, ch, method, delivery, properties, body):
        pass
    

    def update_queue_data(self):
        self._task_queue_obj = self._channel.queue_declare(
            queue=self._task_queue, durable=True,
            exclusive=False, auto_delete=False
        )
        if (self._task_queue_obj):
            self._current_state['replica_count'] = self._docker_client.get_service_replica_count(service_name=self._service_monitor)
            self._current_state['msg_count'] = self._task_queue_obj.method.message_count
            self._current_state['load'] = self._current_state['msg_count'] / (self._current_state['replica_count'] * self._qty_task)
            self._current_state['ligth'] = self.get_ligth(self._current_state['load'])


    def get_ligth(self, load):
        for light in list(self._lights):
            if (load < self._lights[light]):
                return light
        return 'RED'


    def response_to_light(self):
        while (True):
            self.update_queue_data()
            print(BColors.__dict__[self._current_state['ligth']] + f" [+] Workers State - Work Load: {self._current_state['load']:.2f} - Active replicas: {self._current_state['replica_count']} - Msg count: {self._current_state['msg_count']}" + BColors.ENDC)
            if (self._current_state['ligth'] == 'GREY'):
                # Our workers are idle so we kill some
                self.remove_worker()
            elif (self._current_state['ligth'] == 'GREEN'):
                # Our workers are good so we do nothing
                pass
            elif (self._current_state['ligth'] == 'YELLOW'):
                # Our workers are busy so we create more
                self.create_worker()
            elif (self._current_state['ligth'] == 'RED'):
                # Our workers are very busy so we create a lot more (2x)
                self.create_worker(2)
            sleep(10)


    def create_worker(self, scale_step=1):
        scale_to = self._current_state['replica_count'] + scale_step
        if (scale_to <= self._max_scale):
            if (self._debug):
                print(f"Scaling up {self._service_monitor} from {self._current_state['replica_count']} to {scale_to} replicas")
            self._docker_client.scale_service(service_name=self._service_monitor, replica_count=scale_to)


    def remove_worker(self, scale_step=1):
        scale_to = self._current_state['replica_count'] - scale_step
        if (scale_to >= self._min_scale):
            if (self._debug):
                print(f"Scaling down {self._service_monitor} from {self._current_state['replica_count']} to {scale_to} replicas")
            self._docker_client.scale_service(service_name=self._service_monitor, replica_count=scale_to)


    def start(self):
        while True:
            try:
                self._docker_client = DockerAPIClient()
                self._current_state = {
                    'ligth': 'GREEN', 
                    'load': 0.4,
                    'replica_count': self._docker_client.get_service_replica_count(service_name=self._service_monitor)
                }
                self._connection = BlockingConnection(URLParameters(self._amqp_url))
                self._channel = self._connection.channel()
                self.response_to_light()
                self._connection.close()
            except AMQPConnectionError:
                if (self._debug):
                    print(" [!] RabbitMQ Host Unreachable. Reconecting in {} seconds...".format(self._reconection_time))
                sleep(self._reconection_time)
            except Exception as e:
                if (self._debug):
                    print(e)
                sleep(self._reconection_time)


def main():
    """Main entry point to the program."""
    admin = AdminWorker()
    admin.start()


if __name__ == '__main__':
    main()
