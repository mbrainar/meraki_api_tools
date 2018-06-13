import requests
from argparse import ArgumentParser
from utils import get_org_id, get_network_id, get_template_id
import os
import json

def get_current_template(api_key, network_id):
    url = "https://api.meraki.com/api/v0/networks/{}".format(network_id)
    headers = {
        'x-cisco-meraki-api-key': api_key
        }
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        if "configTemplateId" in response.json():
            return response.json()['configTemplateId']
        else:
            return False
    else:
        return None

def bind_template(api_key, network_id, template_id):
    url = "https://api.meraki.com/api/v0/networks/{}/bind".format(network_id)
    headers = {
        'x-cisco-meraki-api-key': api_key,
        'Content-Type': "application/json"
        }
    payload = {"configTemplateId":template_id}
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    return response.status_code

def unbind_template(api_key, network_id):
    url = "https://api.meraki.com/api/v0/networks/{}/unbind".format(network_id)
    headers = {
        'x-cisco-meraki-api-key': api_key
        }
    response = requests.request("POST", url, headers=headers)
    return response.status_code

if __name__ == '__main__':

    parser = ArgumentParser(description='Usage:')
    # script arguments
    parser.add_argument('-k', '--key', type=str, required=False,
                        help="API Key from Meraki Dashboard")
    parser.add_argument('-o', '--organization', type=str, required=True,
                        help="Name of Organization in Meraki Dashboard")
    parser.add_argument('-n', '--network', type=str, required=True,
                        help="Name of Network in Meraki Dashboard")
    parser.add_argument('-t', '--template', type=str, required=True,
                        help="Name of Configuration Template")
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
    template_name = args.template

    print("Getting organization id for: {}".format(organization_name))
    organization_id = get_org_id(api_key, organization_name)
    if not organization_id:
        print("Unable to find organization: {}".format(organization_name))
        print("Check organization name, ensure you have access to organization, check API key")
        exit()
    print("Organization id = {}".format(organization_id))

    print("Getting network id for: {}".format(network_name))
    network_id = get_network_id(api_key, organization_id, network_name)
    if not network_id:
        print("Unable to find network: {}".format(network_name))
        print("Check network name, ensure network is in organization, check API key")
        exit()
    print("Network id = {}".format(network_id))

    print("Getting current template for network")
    current_template_id = get_current_template(api_key, network_id)
    if current_template_id is None:
        print("Unable to get network info")
        exit()
    elif current_template_id is not False:
        print("Current template id = {}".format(current_template_id))
        # todo add conversion to template name

        # Unbind from current template
        print("Start unbind from current template")
        unbind_status = unbind_template(api_key, network_id)
        if unbind_status != 200:
            print("Unable to unbind template")
            exit()
        else:
            print("Successfully unbound template")
    else:
        print("Network is not currently part of a template")

    print("Start bind to new template")
    print("Getting template id for: {}".format(template_name))
    template_id = get_template_id(api_key, organization_id, template_name)
    if not template_id:
        print("Unable to find template: {}".format(template_name))
        print("Check template name, ensure template is in organization, check API key")
        exit()
    print("Template id = {}".format(template_id))
    bind_status = bind_template(api_key, network_id, template_id)
    if bind_status != 200:
        print("Unable to bind template")
        exit()
    else:
        print("Successfully bound template")
