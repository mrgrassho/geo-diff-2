import time
import functools
from pika import BlockingConnection, SelectConnection, URLParameters

class RabbitMQClient(object):

    def __init__(self, client, amqp_url, queues={}, reconection_time=10, prefetch_count=1, debug=True):
        self._amqp_url = amqp_url
        self._queues = queues
        self._reconection_time = reconection_time # 10 seconds
        self._last_timestamps = dict()
        self._prefetch_count = prefetch_count
        self._connection = None
        self._channel = None
        self._debug = debug
        self._client = client
        self._blocking_connection = None
        self._blocking_channel = None


    def message_count(self, name):
        if (name in self._queues and self._blocking_channel):
            queue = self._blocking_channel.queue_declare(
                queue=name,
                durable=self._queues[name]['durable'],
                exclusive=self._queues[name]['exclusive'], 
                auto_delete=self._queues[name]['auto_delete'],
                passive=True
            )
            return queue.method.message_count
        else:
            return None


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
            self._channel.queue_declare(
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
        cb = functools.partial(self.on_qos, userdata=queue_name)
        self._channel.basic_qos(prefetch_count=self._prefetch_count, callback=cb)


    def on_qos(self, _unused_frame, userdata):
        """Callback when Basic.QOS has completed."""
        if (self._debug):
            print(" [x] QOS set to {}".format(self._prefetch_count))
        queue_name = userdata
        self.start_consuming(queue_name)


    def on_message(self, channel, method, properties, body):
        queue_name = method.routing_key
        if (self._queues[queue_name]['callback']):
            callback = getattr(self._client, self._queues[queue_name]['callback'])
            callback(channel, method, properties, body)


    def start_consuming(self, queue_name):
        """Start consuming from task queue."""
        if (self._debug):
            print(" [x] Waiting for messages...")
        self._channel.basic_consume(
            queue_name,
            self.on_message,
            auto_ack=self._queues[queue_name]['auto_ack']
        )


    def start(self):
        """Start worker."""
        connected = False
        # Define connection
        while (not connected):
            try:
                self._blocking_connection = BlockingConnection(URLParameters(self._amqp_url))
                self._blocking_channel = self._blocking_connection.channel()
                self._connection = SelectConnection(URLParameters(self._amqp_url), on_open_callback=self.on_open_connection)
                self._connection.ioloop.start()
                connected = True
            # Catch a Keyboard Interrupt to make sure that the connection is closed cleanly
            except KeyboardInterrupt:
                # Gracefully close the connection
                self._connection.close()
                # Start the IOLoop again so Pika can communicate, it will stop on its own when the connection is closed
                self._connection.ioloop.start()
            except :
                if (self._debug):
                    print(" [!] RabbitMQ Host Unrecheable. Reconnecting in {} seconds...".format(self._reconection_time))
                time.sleep(self._reconection_time)
