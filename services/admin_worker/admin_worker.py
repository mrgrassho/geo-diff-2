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
from datetime import datetime, timedelta
from rabbimq_client import RabbitMQClient
from json import loads
from copy import copy
<<<<<<< HEAD
from random import choices
from ast import literal_eval
=======
>>>>>>> f21729471cdc8a3d7943af31054b6e11918241c3

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
        self._keep_alive_queue = environ['KEEP_ALIVE_QUEUE']
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
        self._min_scale = int(environ['MIN_SCALE'])
        self._service_monitor = environ['SERVICE_MONITOR']
        self._service_dealer = environ['SERVICE_DEALER']
        self._step_batch_dealer = int(environ['STEP_BATCH_DEALER'])
        self._min_batch_dealer = int(environ['MIN_BATCH_DEALER'])
        self._max_batch_dealer = int(environ['MAX_BATCH_DEALER'])
        self._debug = debug
        self._refresh_rate = float(environ['REFRESH_RATE'])
        self._max_timeout = timedelta(seconds=int(environ['MAX_TIMEOUT']))
        self._rabbitmq_client = RabbitMQClient(
            self,
            amqp_url = self._amqp_url,
            queues = {
                self._task_queue: {
                    "durable": True,
                    "exclusive": False,
                    "auto_delete": False,
                    "auto_ack": False,
                    "callback": None
                },
                self._keep_alive_queue: {
                    "durable": True,
                    "exclusive": False,
                    "auto_delete": False,
                    "auto_ack": True,
                    "callback": "callback_keep_alive_queue"
                }
            },
            reconection_time = self._reconection_time,
            prefetch_count = self._prefetch_count,
            debug = self._debug
        )


    def callback_keep_alive_queue(self, ch, method, properties, body):
        data = loads(body)
        worker = data['id']
        if (self._docker_client.get_container(worker)):
            self._last_timestamps[worker] = data['timestamp']


    def update_queue_data(self):
        message_count = self._rabbitmq_client.message_count(self._task_queue)
        if (message_count is not None):
            self._current_state['replica_count'] = self._docker_client.get_service_replica_count(service_name=self._service_monitor)
            self._current_state['msg_count'] = message_count
            self._current_state['load'] = self._current_state['msg_count'] / (self._current_state['replica_count'][0] * self._qty_task)
            self._current_state['ligth'] = self.get_ligth(self._current_state['load'])


    def get_ligth(self, load):
        for light in list(self._lights):
            if (load < self._lights[light]):
                return light
        return 'RED'


    def response_to_light(self):
        count = 0
        while (True):
            self.update_queue_data()
            print(BColors.__dict__[self._current_state['ligth']] + f" [+] Workers State - Work Load: {self._current_state['load']:.2f} - Replicas: {'/'.join([str(i) for i in self._current_state['replica_count']])} - Msg count: {self._current_state['msg_count']}" + BColors.ENDC)
            print(f" [#] {datetime.now().strftime('%H:%M:%S.%f')} {self._current_state['load']:.2f} {self._current_state['ligth']}")
            if (self._current_state['ligth'] == 'GREY'):
                # Our workers are idle so we kill some
                count += 1
                if (count >= 3):
                    self.remove_worker()
                    count = 0
            elif (self._current_state['ligth'] == 'GREEN'):
                # Our workers are good so we do nothing
                count = 0
            elif (self._current_state['ligth'] == 'YELLOW'):
                # Our workers are busy so we create more
                count = 0
                self.create_worker()
            elif (self._current_state['ligth'] == 'RED'):
                # Our workers are very busy so we create a lot more (2x)
                count = 0
                self.create_worker(2)
            sleep(self._refresh_rate)


    def create_worker(self, scale_step=1):
        scale_to = self._current_state['replica_count'][1] + scale_step
        if (scale_to <= self._max_scale):
            if (self._debug):
                print(f"Scaling up {self._service_monitor} from {self._current_state['replica_count'][1]} to {scale_to} replicas")
            self._docker_client.scale_service(service_name=self._service_monitor, replica_count=scale_to)
        else:
            self.update_delivery(-1*self._step_batch_dealer)


    def update_delivery(self, batch=100, wait=None):
        envs = self._docker_client.get_service_env(self._service_dealer)
        if envs is None: return
        if self._min_batch_dealer <= literal_eval(envs['BATCH']) + batch <= self._max_batch_dealer:
            if (self._debug): print(f"Updating {self._service_dealer}. BATCH += {batch} and WAIT += {wait} ")
            self._docker_client.update_service_env_add(
                self._service_dealer,
                new_env= {
                    'BATCH': batch,
                    'WAIT': wait,
                }
            )


    def remove_worker(self, scale_step=1):
        scale_to = self._current_state['replica_count'][1] - scale_step
        if (scale_to >= self._min_scale):
            if (self._debug):
                print(f"Scaling down {self._service_monitor} from {self._current_state['replica_count'][1]} to {scale_to} replicas")
            self._docker_client.scale_service(service_name=self._service_monitor, replica_count=scale_to)


    def calculate_timeout_workers(self):
        # Calculo si algun worker lleva demasiado tiempo sin responder
        while (True):  # recorro array con workers y sus tiempos.
            p = None
            if (len(self._last_timestamps) > 0 and self._debug):
                p = f"{'-'*80}\n{BColors.GREY}\tWORKER\t\tLAST SEEN\t\t\tSTATUS\t{BColors.ENDC}\n"
            last_timestamps_tmp = copy(self._last_timestamps)
            removed_workers = []
            for worker, timestamp in last_timestamps_tmp.items():
                timeout_worker = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
                diff = datetime.now() - timeout_worker
                container = self._docker_client.get_container(worker)
                if (not container):
                    removed_workers.append((worker, 0))
                else:
                    if (diff > self._max_timeout):
                        status = ('NOT RESPONDING', BColors.RED) 
                        if (container):
                            container.remove()
                        removed_workers.append((worker, 1))
                    elif (diff > self._max_timeout/2): # excede la mitad del tiempo de timeout
                        status = ('WARNING', BColors.YELLOW) 
                    else:
                        status = ('OK', BColors.GREEN) 
                    if (self._debug):
                        p += f"\t{status[1]}{worker}\t{timestamp}\t{status[0]}\t{BColors.ENDC}\n"
            if (self._debug and p is not None):
                print(p)
            for removed_worker in removed_workers:
                self._last_timestamps.pop(removed_worker[0])
                if (self._debug and removed_worker[1] == 1):
                    print(f' [!] Worker {removed_worker[0]} is NOT responding.')
                    print(f' [+] Worker {removed_worker[0]} removed.')
            sleep(self._refresh_rate)


    def start(self):
        t3 = Thread(target=self._rabbitmq_client.start)
        t3.start()
        self._docker_client = DockerAPIClient()
        self._current_state = {
            'msg_count': -1,
            'ligth': 'GREEN', 
            'load': 0.4,
            'replica_count': self._docker_client.get_service_replica_count(service_name=self._service_monitor)
        }
        t1 = Thread(target=self.response_to_light)
        t1.start()
        t2 = Thread(target=self.calculate_timeout_workers)
        t2.start()


def main():
    """Main entry point to the program."""
    admin = AdminWorker()
    admin.start()


if __name__ == '__main__':
    main()
