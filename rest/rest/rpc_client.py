import pika
import uuid
import ConfigParser

class rpc_client(object):
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

        self.queue_name_ = queue_name

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port, credentials=credentials))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.request_id_ == props.correlation_id:
            print 'on response. body={}'.format(body)
            self.response_ = body

    def send_data(self, data):
        self.response_ = None
        self.request_id_ = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name_,
                                   properties=pika.BasicProperties(
                                           reply_to=self.callback_queue,
                                           correlation_id=self.request_id_,
                                   ),
                                   body=data)

        while self.response_ is None:
            self.connection.process_data_events()

        print 'response from send data={}'.format(self.response_)

        return int(self.response_)