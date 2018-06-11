import requests
from argparse import ArgumentParser
from utils import get_org_id, get_network_id
import os
import json

def get_vlans(api_key, network_id, vlan_id):
    if vlan_id:
        url = "https://api.meraki.com/api/v0/networks/{}/vlans/{}".format(network_id, vlan_id)
    else:
        url = "https://api.meraki.com/api/v0/networks/{}/vlans".format(network_id)
    headers = {
        'x-cisco-meraki-api-key': api_key,
        'Cache-Control': "no-cache",
        'Postman-Token': "cab4c162-203e-4cc6-bff1-42d946026c15"
        }
    response = requests.request("GET", url, headers=headers)
    if vlan_id and response.status_code == 404:
        print("VLAN ID provided was not found in the network")
        return False
    else:
        return response.json()

if __name__ == '__main__':

    parser = ArgumentParser(description='Usage:')
    # script arguments
    parser.add_argument('-k', '--key', type=str, required=False,
                        help="API Key from Meraki Dashboard")
    parser.add_argument('-o', '--organization', type=str, required=True,
                        help="Name of Organization in Meraki Dashboard")
    parser.add_argument('-n', '--network', type=str, required=True,
                        help="Name of Network in Meraki Dashboard")
    parser.add_argument('-v', '--vlan', type=str, required=False,
                        help="Only return information for the VLAN provided")
    parser.add_argument('-f', '--file', type=str, required=False,
                        help="Output file for VLAN information")
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
    if args.vlan:
        vlan_id = args.vlan
    else:
        vlan_id = False
    network_name = args.network
    if args.file:
        output_file = args.file
    else:
        output_file = False

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

    if vlan_id:
        print("Getting information VLAN {}".format(vlan_id))
    else:
        print("Getting information for all VLANs")

    vlan_details = get_vlans(api_key, network_id, vlan_id)
    if vlan_details:
        if output_file:
            print("Output file provided, writing to {}".format(output_file))
            fh = open(output_file,"w")
            json.dump(vlan_details, fh)
            print("Writing complete")
            fh.close()
        else:
            print("Pretty printing VLAN details")
            print(json.dumps(vlan_details, sort_keys=True, indent=4))
