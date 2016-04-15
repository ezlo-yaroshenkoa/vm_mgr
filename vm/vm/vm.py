import libvirt
from mako.template import Template

def create(name, br=None):
    vm_template = Template(filename='./template.xml')

    args = dict()

    args['vm_name'] = name

    if (br):
        args['br_name'] = br

    vm_template_data = vm_template.render(**args)

    conn = libvirt.open('qemu:///system')

    conn.defineXML(vm_template_data)

def delete(name):
    domain = find_domain(name)
    domain.undefine()

def power_on(name):
    domain = find_domain(name)
    domain.create()

def power_off(name):
    domain = find_domain(name)
    domain.shutdown()

def reboot(name):
    domain = find_domain(name)
    domain.reboot()

def reset(name):
    domain = find_domain(name)
    domain.reset()

def destroy(name):
    domain = find_domain(name)
    domain.destroy()

def find_domain(name):
    conn = libvirt.open('qemu:///system')
    return conn.lookupByName(name)