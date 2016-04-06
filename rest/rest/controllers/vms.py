from pecan import expose
from pecan.rest import RestController
from power import PowerController
from rest.rpc_client import RpcClient

class VmsController(RestController):

    power = PowerController()

    @expose()
    def get_all(self):
        return 'vms controller. get_all'

    @expose()
    def get_one(self, vm_name):
        return 'vms controller. get_one. vm_name={}'.format(vm_name)

    @expose()
    def post(self, vm_name, **data):
        response = 'vms controller. post. vm_name={}'.format(vm_name)

        br = data.get('br')

        if br:
            response += '. br={}'.format(br)

        return response

    @expose()
    def delete(self, vm_name):
        return 'vms controller. delete. vm_name={}'.format(vm_name)