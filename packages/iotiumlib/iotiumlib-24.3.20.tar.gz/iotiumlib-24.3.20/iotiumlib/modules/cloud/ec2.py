"""
// ========================================================================
// Copyright (c) 2020 IoTium. All Rights Reserved.
// ------------------------------------------------------------------------
// All rights reserved.
//
// ========================================================================
"""

__author__ = "Rashtrapathy"
__copyright__ = "Copyright (c) 2020 IoTium. All Rights Reserved."
__license__ = "All rights reserved."
__email__ = "rashtrapathy.c@iotium.io"

import configparser
import os

import boto3
from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider


class CloudAction(object):
    def __init__(self):
        try:
            cls = get_driver(Provider.EC2)
            ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
            SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
            REGION = os.getenv('AWS_DEFAULT_REGION')
            self.driver = cls(ACCESS_KEY_ID, SECRET_ACCESS_KEY, region=REGION)
            print('AWS resource connected.')
        except Exception as err:
            print(f'AWS resource not connected.{err}')

    def __del__(self):
        pass


class AwsBoto3Call(object):
    def __init__(self):
        # Retrieve AWS credentials and region from environment variables
        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        aws_region = os.environ.get('AWS_DEFAULT_REGION')

        # Create a session using the environment variables
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )
        self.ec2_client = session.client('ec2')


def get_instace_id(private_ip_address):
    if private_ip_address is None:
        print('Private IP address if not set.')
        return False

    # Specify the private IP address
    private_ip_address = private_ip_address

    # Describe instances filtering by the private IP address
    response = AwsBoto3Call().ec2_client.describe_instances(
        Filters=[
            {
                'Name': 'network-interface.addresses.private-ip-address',
                'Values': [private_ip_address]
            }
        ]
    )
    current_instance_id = None
    # Extract the instance ID from the response
    if 'Reservations' in response:
        reservations = response['Reservations']
        if reservations:
            instances = reservations[0]['Instances']
            if instances:
                instance = instances[0]
                current_instance_id = instance['InstanceId']
                print("Current Instance ID:", current_instance_id)
                return current_instance_id
            else:
                print("No instances found for the given private IP address")
                return None
        else:
            print("No reservations found for the given private IP address")
            return None
    else:
        print("Error occurred while describing instances")
        return None


def update_route_table(route_table_id, old_instance_id, new_instance_id):
    print("Processing Route Table:", route_table_id)

    # Specify the current instance ID (Instance X) and the new instance ID (Instance Y)
    new_instance_id = new_instance_id

    # Describe route tables in the VPC
    response = AwsBoto3Call().ec2_client.describe_route_tables(
        Filters=[
            {
                'Name': 'route.instance-id',
                'Values': [old_instance_id]
            }
        ],
        RouteTableIds=[
            route_table_id,
        ]
    )

    # Extract the route table IDs from the response
    if 'RouteTables' in response:
        route_tables = response['RouteTables']
        if route_tables:
            for route_table in route_tables:
                # route_table_id = route_table['RouteTableId']
                # print("Processing Route Table:", route_table_id)

                # Get the routes associated with the current instance
                routes_to_update = [
                    route for route in route_table['Routes']
                    if 'InstanceId' in route and route['InstanceId'] == old_instance_id
                ]

                # Update the routes to point to the new instance
                for route in routes_to_update:
                    response = AwsBoto3Call().ec2_client.replace_route(
                        RouteTableId=route_table_id,
                        DestinationCidrBlock=route['DestinationCidrBlock'],
                        InstanceId=new_instance_id
                    )

                    # Check for errors in the response
                    if 'Errors' in response:
                        print("Error occurred while updating route in Route Table:", route_table_id)
                        print(response['Errors'])
                    else:
                        print("Route updated successfully in Route Table:", route_table_id)
        else:
            print("No route tables found associated with the current instance")
    else:
        print("Error occurred while describing route tables")


def get_route_tables(vpc):
    try:
        filters = {'vpc-id': [vpc]}
        response = CloudAction().driver.ex_list_route_tables(filters=filters)
        op = list()
        for key in response:
            name = '-'
            if 'tags' in key.extra and 'Name' in key.extra['tags']:
                name = key.extra['tags']['Name']
            op.append({'Name': name, 'Id': key.id})
        print(op)
    except Exception as err:
        print("Error in getting route tables {}".format(err))


def check_image_exists(image_id):
    print('Checking image availability.')
    images = CloudAction().driver.list_images()
    for image in images:
        if (image.id == image_id):
            return True
    return False


def get_keys():
    print('Listing Key(s)')
    keypairs = CloudAction().driver.list_key_pairs()
    op = list()
    for key in keypairs:
        op.append({'Name': key.name})
    print(op)


def get_vpc():
    print('Listing VPC(s)')
    response = CloudAction().driver.ex_list_networks()
    op = list()
    for key in response:
        name = '-'
        if 'tags' in key.extra and 'Name' in key.extra['tags']:
            name = key.extra['tags']['Name']
        op.append({'Name': name, 'Id': key.id, 'Cidr': key.cidr_block})
    print(op)


def get_security_group_ids(security_groups):
    sgs = CloudAction().driver.ex_get_security_groups(group_names=security_groups)
    return_list = []
    for sg in sgs:
        return_list.append(sg.id)
    return return_list


def get_subnet(vpc):
    print('Listing Subnets(s) in VPC {}'.format(vpc))
    filters = {'vpc-id': [vpc]}
    response = CloudAction().driver.ex_list_subnets(filters=filters)
    op = list()
    for key in response:
        op.append({'CIDR Block': key.extra['cidr_block'], 'Subnet Id': key.id, 'State': key.state,
                   'VPC Id': key.extra['vpc_id']})
    print(op)


def get_image_id():
    print('Listing AMI(s)')
    response = CloudAction().driver.list_images(ex_owner='306231577965')
    op = list()
    for key in response:
        op.append({'AMI Id': key.id, 'Name': key.name})
    print(op)


def check_key_name_exists(key_name):
    response = CloudAction().driver.list_key_pairs()
    for key in response:
        if key.name == key_name:
            return True
    print("Key {} not found".format(key_name))
    return False


def createInstanceWrapper(row):
    # global data
    region = None

    key = row['key_name'] if 'key_name' in row and row['key_name'] else ""
    flavour = row['instance_type'] if 'instance_type' in row and row['instance_type'] else 'm1.small'
    sgi = row['security_group_ids'] if 'security_group_ids' in row and row['security_group_ids'] else []
    subnet = row['subnet_id'] if 'subnet_id' in row and row['subnet_id'] else ""

    if not isinstance(sgi, list):
        return False

    user_data = row['cert_file'] if 'cert_file' in row else None
    if user_data is not None and os.path.isfile(user_data):
        with open(user_data, 'r') as f:
            ud = f.read().strip()
        image_id = row['image_id'] if 'image_id' in row and row['image_id'] else None
    else:
        ud = None
        print("Cert file not present.")
        return False

    if key:
        if check_key_name_exists(key):
            if image_id:
                # print('AMI ID found for launching')
                op = createInstance(image_id, region, key, flavour, sgi, subnet, ud,
                                    tag_name=row['NodeName'])
                if op:
                    print('Instance Info: {}'.format(op))
                    return op['instance_id']
                else:
                    print('No instance info found.')
                    return False
            else:
                print('Mandatory AMI ID info not found in YAML config.')
                return False
        else:
            print('SSH key-pair info not found in the region.')
            print('TODO: can create new info.')
            return False
    else:
        print('Mandatory key-pair info not found in YAML config.')
        return False


def createInstance(image_id, placement_group=None, key_name=None, instance_type=None, security_group_ids=None,
                   subnet_id=None, user_data=None, tag_name='OtaTool'):
    print("Launching Instance {}".format(tag_name))
    try:
        subnets = CloudAction().driver.ex_list_subnets(subnet_ids=[subnet_id])
        sizes = CloudAction().driver.list_sizes()
        if check_image_exists(image_id):
            print("Image Id Found")
            images = CloudAction().driver.list_images(ex_image_ids=[image_id])
        else:
            print("Image Id not found")
            return False

        size = [s for s in sizes if s.id == instance_type][0]
        image = [i for i in images if i.id == image_id][0]
        subnet = [sn for sn in subnets if sn.id == subnet_id][0]

        # Precedence to id and then name
        if security_group_ids != []:
            sg_ids = security_group_ids
        else:
            return False

        instance = CloudAction().driver.create_node(name=tag_name, size=size,
                                                    image=image,
                                                    ex_userdata=user_data,
                                                    ex_keyname=key_name,
                                                    ex_security_group_ids=sg_ids,
                                                    ex_subnet=subnet
                                                    )
        print('Instance created. Wait until running')
        [instance_details] = CloudAction().driver.wait_until_running([instance])
        print('Refreshing the Instance')
        instance = instance_details[0]
        sourceDestChk = CloudAction().driver.ex_modify_instance_attribute(instance,
                                                                          attributes={'SourceDestCheck.Value': False})
        if not sourceDestChk:
            print("Disabling source destination check failed")
        return {"public_ip_address": instance.public_ips, "public_dns_name": instance.extra['dns_name'],
                "instance_id": instance.id}
    except Exception as err:
        print('Launch failed. {}'.format(err))
        return {}
