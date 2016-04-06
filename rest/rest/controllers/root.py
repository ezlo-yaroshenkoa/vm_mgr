from pecan import expose
from pecan.rest import RestController

class PowerController(RestController):

    @expose()
    def post(self, vm_name, power_action):
        return 'power controller. vm_name={}. power_action={}'.format(vm_name, power_action)

class VmsController(RestController):

    power = PowerController()

    @expose()
    def get(self):
        return 'vms controller. get_all'

    @expose()
    def get_one(self, vm_name):
        return 'vms controller. get_one. vm_name={}'.format(vm_name)

    @expose()
    def post(self, vm_name):
        return 'vms controller. post. vm_name={}'.format(vm_name)

    @expose()
    def delete(self, vm_name):
        return 'vms controller. delete. vm_name={}'.format(vm_name)

class RootController(object):

    vms = VmsController()