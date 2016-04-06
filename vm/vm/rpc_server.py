import pika
import ConfigParser
from pyroute2.iproute import IPRoute
import json

class RpcServer(object):
    def __init__(self):
        config = ConfigParser.RawConfigParser()

        config.read('config.cfg')

        section_name = 'rabbitmq_server'

        host = config.get(section_name, 'host')
        port = int(config.get(section_name, 'port'))
        user_name = config.get(section_name, 'user_name')
        password = config.get(section_name, 'password')
        queue_name = config.get(section_name, 'queue_name')

        credentials = pika.PlainCredentials(user_name, password)

        self.connection_ = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port, credentials=credentials))

        self.channel_ = self.connection_.channel()

        self.channel_.queue_declare(queue=queue_name)
        self.channel_.basic_qos(prefetch_count=1)
        self.channel_.basic_consume(self.on_request, queue=queue_name)

    def on_request(self, channel, method, props, body):
        response = 0

        obj = json.loads(body)

        action = obj['action']
        bridge_name = obj['bridge_name']

        print 'on request. action={}, bridge_name={}'.format(action, bridge_name)

        if action == 0:
            response = self.create_bridge(bridge_name)
        elif action == 1:
            response = self.delete_bridge(bridge_name)

        print 'response={}'.format(response)

        channel.basic_publish(exchange='',
                              routing_key=props.reply_to,
                              properties=pika.BasicProperties(correlation_id=props.correlation_id),
                              body=str(response))

        channel.basic_ack(delivery_tag=method.delivery_tag)

    def create_bridge(self, bridge_name):
        try:
            ip = IPRoute()
            ip.link_create(ifname=bridge_name, kind='bridge')
            return 1
        finally:
            return 0

    def delete_bridge(self, bridge_name):
        try:
            ip = IPRoute()
            idx = ip.link_lookup(ifname=bridge_name)[0]
            ip.link_remove(idx)
            return 1
        finally:
            return 0

    def start(self):
        self.channel_.start_consuming()