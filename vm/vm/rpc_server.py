import pika
import ConfigParser
import vm
import json
from libvirt import libvirtError

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
        obj = json.loads(body)

        command = obj['command']

        response = 1

        try:
            if command == 'create':
                vm.create(obj['vm'], obj['br'])
            elif command == 'delete':
                vm.delete(obj['vm'])
            elif command == 'power':
                self.power_wm(obj['vm'], obj['power_action'])
            else:
                response = 0
                print 'unknown command. command={}'.format(command)
        except libvirtError as err:
            response = 0
            print err

        channel.basic_publish(exchange='',
                              routing_key=props.reply_to,
                              properties=pika.BasicProperties(correlation_id=props.correlation_id),
                              body=str(response))

        channel.basic_ack(delivery_tag=method.delivery_tag)

    def power_vm(self, name, action):
        if action == 'on':
            vm.power_on(name)
        elif action == 'off':
            vm.power_off(name)
        elif action == 'reboot':
            vm.reboot(name)

    def start(self):
        self.channel_.start_consuming()