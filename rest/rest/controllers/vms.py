from pecan import expose, abort
from pecan.rest import RestController
from power import PowerController
import json
from rest.rpc_client import rpc_client
from rest.vms_db import vms_db

class VmsController(RestController):

    power = None

    def __init__(self):
        self.vms_db_ = vms_db()
        self.rpc_client_ = rpc_client()
        self.power = PowerController(self.rpc_client_)

    @expose()
    def get(self):
        return self.vm_db_.get_all()

    @expose()
    def post(self, vm_name, **data):
        data_to_send = dict()
        data_to_send['command'] = 'create'
        data_to_send['vm'] = vm_name

        br = data.get('br')

        if br:
            data_to_send['br'] = br

        json_data = json.dumps(data_to_send)

        result = self.rpc_client_.send_data(json_data)

        print 'create vm result={}'.format(result)

        if result:
            self.vm_db_.add(vm_name)
        else:
            abort(500)

        return 'vm created. vm_name={}'.format(vm_name)

    @expose()
    def delete(self, vm_name):
        data = dict()
        data['command'] = 'delete'
        data['vm'] = vm_name

        json_data = json.dumps(data)

        result = self.rpc_client_.send_data(json_data)

        print 'delete vm result={}'.format(result)

        if result:
            self.vm_db_.delete(vm_name)
        else:
            abort(500)

        return 'vm deleted. vm_name={}'.format(vm_name)