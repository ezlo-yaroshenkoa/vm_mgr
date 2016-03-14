import argparse

def create_vm(params):
    print 'create vm. name={}. br={}'.format(params.name, params.br)
    pass

def delete_vm(params):
    print 'delete vm. name={}. br={}'.format(params.name, params.br)
    pass

def manage_power(params):
    pass

def list_vm():
    pass

def parse_cmd_line():
    parser = argparse.ArgumentParser(description='process command line')

    subparsers = parser.add_subparsers(help='commands subparsers')

    parser_create = subparsers.add_parser('create')
    parser_create.add_argument('-vm', type=str, help='vm name', required=True)
    parser_create.add_argument('-br', type=str, help='bridge name')
    parser_create.set_defaults(func=create_vm)

    parser_delete = subparsers.add_parser('delete')
    parser_delete.add_argument('-vm', type=str, help='vm name', required=True)
    parser_delete.set_defaults(func=delete_vm)

    parser_power = subparsers.add_parser('power')
    parser_power.add_argument('-vm', type=str, help='vm name', required=True)
    parser_power.add_argument('-on', action='store_true', help='power on')
    parser_power.add_argument('-off', action='store_true', help='power off')
    parser_power.add_argument('-reboot', action='store_true', help='reboot')
    parser_power.set_defaults(func=manage_power)

    args = parser.parse_args()

    args.func(args)

if __name__ == '__main__':
    parse_cmd_line()