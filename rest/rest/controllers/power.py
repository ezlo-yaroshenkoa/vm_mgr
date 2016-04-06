from pecan import expose
from pecan.rest import RestController
from rest.rpc_client import RpcClient

class PowerController(RestController):

    @expose()
    def post(self, vm_name, power_action):
        return 'power controller. vm_name={}. power_action={}'.format(vm_name, power_action)