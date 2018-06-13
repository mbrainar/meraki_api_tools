import requests

# Get the organization id from the provided name
def get_org_id(api_key, organization_name):
    url = "https://api.meraki.com/api/v0/organizations"
    headers = {
        'x-cisco-meraki-api-key': api_key
        }
    response = requests.request("GET", url, headers=headers)

    for org in response.json():
        if org['name'] == organization_name:
            return org['id']

def get_network_id(api_key, organization_id, network_name):
    url = "https://api.meraki.com/api/v0/organizations/{}/networks".format(organization_id)
    headers = {
        'x-cisco-meraki-api-key': api_key
    }
    response = requests.request("GET", url, headers=headers)

    for network in response.json():
        if network['name'] == network_name:
            return network['id']

def get_template_id(api_key, organization_id, template_name):
    url = "https://api.meraki.com/api/v0/organizations/{}/configTemplates".format(organization_id)
    headers = {
        'x-cisco-meraki-api-key': api_key
    }
    response = requests.request("GET", url, headers=headers)

    for template in response.json():
        if template['name'] == template_name:
            return template['id']
