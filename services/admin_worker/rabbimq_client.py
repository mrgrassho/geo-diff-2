import time
from pika import SelectConnection, URLParameters

class RabbitMQClient(object):

    def __init__(self, amqp_url, queues={}, reconection_time=10, prefetch_count=1, debug=True):
        self._amqp_url = amqp_url
        self._queues = queues
        self._reconection_time = reconection_time # 10 seconds
        self._last_timestamps = dict()
        self._prefetch_count = prefetch_count
        self._connection = None
        self._channel = None
        self._debug = debug

    
    def queue_obj(self, name):
        return self._queues[name]['obj']


    def on_open_connection(self, _unused_frame):
        if (self._debug):
            print(" [x] Connected - Connection state: OPEN. ")
        self._connection.channel(on_open_callback=self.on_channel_open)


    def on_channel_open(self, channel):
        """Callback when we have successfully declared the channel."""
        if (self._debug):
            print(" [x] Channel - Channel state: OPEN. ")
        self._channel = channel
        for key, queue in self._queues.items():
            cb = functools.partial(self.on_queue_declareok, userdata=key)
            self._queues[key]['obj'] = self._channel.queue_declare(
                queue=key, 
                durable=queue['durable'], 
                exclusive=queue['exclusive'], 
                auto_delete=queue['auto_delete'],
                callback=cb
            )


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


    def on_qos(self, _unused_frame):
        """Callback when Basic.QOS has completed."""
        if (self._debug):
            print(" [x] QOS set to {}".format(self._prefetch_count))
        self.start_consuming()


    def start_consuming(self):
        """Start consuming from task queue."""
        if (self._debug):
            print(" [x] Waiting for messages...")
        for key, queue in self._queues.items():
            self._channel.basic_consume(
                key, 
                queue['callback'], 
                auto_ack=queue['auto_ack']
            )


    def start(self):
        """Start worker."""
        # Define connection
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
            time.sleep(self._reconection_time)