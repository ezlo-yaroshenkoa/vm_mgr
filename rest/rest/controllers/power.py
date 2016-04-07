from pecan import expose, abort
from pecan.rest import RestController
import json

class PowerController(RestController):
    rpc_client_ = None

    def __init__(self, rpc_client):
        self.rpc_client_ = rpc_client

    @expose()
    def post(self, vm_name, power_action):
        data = dict()
        data['command'] = 'power'
        data['vm'] = vm_name
        data['power_action'] = power_action

        json_data = json.dumps(data)

        result = self.rpc_client_.send_data(json_data)

        print 'power. vm_name={}. action={}. result={}'.format(vm_name, power_action, result)

        if False == result:
            abort(500)

        return 'vm created. vm_name={}'.format(vm_name)