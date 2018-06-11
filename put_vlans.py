import requests
from argparse import ArgumentParser
from utils import get_org_id, get_network_id
import os
import json

def put_vlan(api_key, network_id, vlan_id, vlan_details):
    url = "https://api.meraki.com/api/v0/networks/{}/vlans/{}".format(network_id, vlan_id)
    # print(url)
    headers = {
        'x-cisco-meraki-api-key': api_key,
        'Cache-Control': "no-cache",
        'Postman-Token': "cab4c162-203e-4cc6-bff1-42d946026c15"
        }
    payload = vlan_details
    response = requests.request("PUT", url, json=payload, headers=headers)
    return response.status_code, response.json()

if __name__ == '__main__':

    parser = ArgumentParser(description='Usage:')
    # script arguments
    parser.add_argument('-k', '--key', type=str, required=False,
                        help="API Key from Meraki Dashboard")
    parser.add_argument('-o', '--organization', type=str, required=True,
                        help="Name of Organization in Meraki Dashboard")
    parser.add_argument('-n', '--network', type=str, required=True,
                        help="Name of Network in Meraki Dashboard")
    parser.add_argument('-f', '--file', type=str, required=True,
                        help="Input file for VLAN information")
    args = parser.parse_args()

    if args.key:
        api_key = args.key
        print("Using API Key provided")
    else:
        print("No API key provided, checking environment variable \"MERAKI_API_KEY\"")
        api_key = os.environ.get("MERAKI_API_KEY")
        if not api_key:
            print("Unable to get API key; exiting")
            exit()
    organization_name = args.organization
    network_name = args.network
    input_file = args.file

    print("Getting organization id for: {}".format(organization_name))
    organization_id = get_org_id(api_key, organization_name)
    if organization_id:
        print("Organization id = {}".format(organization_id))
    else:
        print("Unable to find organization: {}".format(organization_name))
        print("Check organization name, ensure you have access to organization, check API key")
        exit()

    print("Getting network id for: {}".format(network_name))
    network_id = get_network_id(api_key, organization_id, network_name)
    if network_id:
        print("Network id = {}".format(network_id))
    else:
        print("Unable to find network: {}".format(network_name))
        print("Check network name, ensure network is in organization, check API key")
        exit()

    print("Opening input file {}".format(input_file))
    fh = open(input_file, "r")
    vlan_details = json.load(fh)
    if type(vlan_details) is dict:
        print("Input file only contains one vlan; converting dict to list")
        new_vlan_details = []
        new_vlan_details.append(vlan_details)
        vlan_details = new_vlan_details
    print("Looping through vlan list")

    for vlan in vlan_details:
        print("VLAN {} found; putting vlan information".format(vlan['id']))
        # print(json.dumps(vlan, sort_keys=True, indent=4))
        status, response = put_vlan(api_key, network_id, vlan['id'], vlan)
        if status != 200:
            print("There was an error setting the vlan information")
            print(status)
            print(json.dumps(response))
        else:
            print("Successfully set information for vlan {}".format(vlan['id']))

    # print(json.dumps(vlan_details, sort_keys=True, indent=4))
