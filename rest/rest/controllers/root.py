from pecan import expose

class RootController(object):
    @expose(generic=True, template='json')
    def vm(self):
        return 'get vm list'

    @vm.when(method='POST')
    def create_vm(self, vm_name, **data):
        return 'vm {} added. params={}'.format(vm_name, data['test'])

    @vm.when(method='DELETE')
    def delete_vm(self, vm_name):
        return 'vm {} deleted'.format(vm_name)