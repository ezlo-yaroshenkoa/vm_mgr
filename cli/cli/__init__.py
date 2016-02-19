import argparse

def create_vm(parameters):
    pass

def delete_vm():
    pass

def power_off_vm():
    pass

def power_on_vm():
    pass

def reboot_vm():
    pass

def list_vm():
    pass

def parse_cmd_line():
    parser = argparse.ArgumentParser(description='process command line')

    parser.add_argument('--delete', dest='delete', type=str, help='--delete <vm_name>')
    subparsers = parser.add_subparsers(help='subparsers')

    create_parser = subparsers.add_parser('create', help='create')
    #create_parser.add_argument('--create', dest='create', action='store_true', help='')
    create_parser.add_argument('--name', dest='name', type=str, help='')
    create_parser.add_argument('--br', dest='br', type=str, help='')

    # parser.add_argument('--create', dest='create', nargs=2, type=str, help='--create <parameters>')
    #parser.add_argument('--delete', dest='delete', type=str, help='--delete <vm_name>')
    # parser.add_argument('--power-on', dest='power_on', type=str, help='--power-on <vm_name>')
    # parser.add_argument('--power-off', dest='power_off', type=str, help='--power-off <vm_name>')
    # parser.add_argument('--reboot', dest='reboot', type=str, help='--reboot <vm_name>')
    # parser.add_argument('--shutdown', dest='shutdown', type=str, help='--shutdown <vm_name>')
    # parser.add_argument('--list', dest='list', action='store_true', help='--list')

    args = parser.parse_args()

    if args.create:
        create_vm(args.create)
    elif args.delete:
        delete_vm(args.delete)
    elif args.power_off:
        power_off_vm()
    elif args.power_on:
        power_on_vm(args.power_on)
    elif args.reboot:
        reboot_vm()
    elif args.list:
        list_vm()

if __name__ == '__main__':
    parse_cmd_line()