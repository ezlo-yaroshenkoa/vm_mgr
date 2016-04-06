import argparse
import ConfigParser
import requests

def create_vm(params):
    url = get_rest_server_url('vms/{}/power/on').format(params.vm)

    try:
        #data = {'test': 't1'}
        response = requests.post(url)
        print response.text
    except requests.RequestException as e:
        print e

def delete_vm(params):
    url = get_rest_server_url('vm/{}').format(params.vm)

    try:
        response = requests.delete(url)
        print response.text
    except requests.RequestException as e:
        print e

def manage_power(params):
    pass

def list_vm(params):
    url = get_rest_server_url('vm')

    try:
        response = requests.get(url)
        print response.text
    except requests.RequestException as e:
        print e

def get_rest_server_url(request_name):
    config = ConfigParser.RawConfigParser()

    config.read('./../config.cfg')

    section_name = 'rest_server'

    host = config.get(section_name, 'host')
    port = config.get(section_name, 'port')

    request = 'http://{}:{}/{}'.format(host, port, request_name)

    return request

def parse_cmd_line():
    parser = argparse.ArgumentParser(description='process command line')

    subparsers = parser.add_subparsers(help='commands subparsers')

    parser_list = subparsers.add_parser('list')
    parser_list.set_defaults(func=list_vm)

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