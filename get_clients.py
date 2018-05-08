import requests
from argparse import ArgumentParser
from utils import get_org_id

# Get the list of networks in the organization
def get_networks(api_key, organization_id):
    url = "https://api.meraki.com/api/v0/organizations/{}/networks".format(organization_id)
    headers = {
      'x-cisco-meraki-api-key': api_key,
      'Cache-Control': "no-cache",
      'Postman-Token': "609d14d7-2d33-4a2f-bfa7-caaf4e29c595"
      }
    response = requests.request("GET", url, headers=headers)

    return response.json()

# Get list of devices for a given network id
def get_devices(api_key, network_id):
    url = "https://api.meraki.com/api/v0/networks/{}/devices".format(network_id)
    headers = {
    'x-cisco-meraki-api-key': api_key,
    'Cache-Control': "no-cache",
    'Postman-Token': "0076cb43-cd93-49cb-8903-58ce69718bef"
    }
    response = requests.request("GET", url, headers=headers)

    return response.json()

# Get list of clients for a given device
def get_clients(api_key, device_serial, timespan):
    url = "https://api.meraki.com/api/v0/devices/{}/clients".format(device_serial)
    querystring = {"timespan":timespan}
    headers = {
        'x-cisco-meraki-api-key': api_key,
        'Cache-Control': "no-cache",
        'Postman-Token': "385091b4-e733-4f7b-a203-6d06b85ade36"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.json()


if __name__ == '__main__':

    parser = ArgumentParser(description='Usage:')
    # script arguments
    parser.add_argument('-k', '--key', type=str, required=True,
                        help="API Key from Meraki Dashboard")
    parser.add_argument('-o', '--organization', type=str, required=True,
                        help="Name of Organization in Meraki Dashboard")
    parser.add_argument('-t', '--timespan', type=str, required=False,
                        help="Timespan in seconds for which to collect clients")
    parser.add_argument('-v', '--vlan', type=str, required=False,
                        help="Only return clients on the VLAN provided")
    args = parser.parse_args()

    api_key = args.key
    organization_name = args.organization
    if args.timespan:
        timespan = args.timespan
        print("Timespan for connected clients set to {}".format(timespan))
    else:
        timespan = "604800"
        print("Timespan for connected clients not provided, defaulting to {}".format(timespan))
    if args.vlan:
        vlan = args.vlan
        print("Will only return clients for VLAN {}".format(vlan))
    else:
        vlan = None

    all_clients = []
    unique_clients = []

    # Get organization id
    print("Getting organization id for: {}".format(organization_name))
    organization_id = get_org_id(api_key, organization_name)
    if organization_id:
        print("Organization id = {}".format(organization_id))
    else:
        print("Unable to find organization: {}".format(organization_name))
        print("Check organization name, ensure you have access to organization, check API key")
        exit()

    # Get list of networks
    print("Getting list of networks")
    networks = get_networks(api_key, organization_id)
    print("Found {} networks".format(len(networks)))

    # Iterate through networks to get devices in each network
    print("Getting devices for each network")
    for n in networks:
        print("  Getting devices for the network: {}".format(n['name']))
        devices = get_devices(api_key, n['id'])
        print("  Found {} devices".format(len(devices)))

        # Iterate through devices to get clients
        for d in devices:
            if d['model'][:2] == "MX":
                print("    Getting clients associated with the device SN {}".format(d['serial']))
                clients = get_clients(api_key, d['serial'], timespan)

                # Iterate through clients, if VLAN provided, only print matches
                client_count = 0
                client_list = []
                for c in clients:
                    if not vlan:
                        client_count += 1
                        client_list.append(c['mac'])
                        all_clients.append(c['mac'])
                        if c['mac'] not in unique_clients:
                            unique_clients.append(c['mac'])
                    else:
                        if str(c['vlan']) == vlan:
                            client_count += 1
                            client_list.append(c['mac'])
                            all_clients.append(c['mac'])
                            if c['mac'] not in unique_clients:
                                unique_clients.append(c['mac'])
                print("    Found {} clients".format(client_count))
                # print("    {}".format(client_list))

            else:
                print("    Skipping device SN {}, not MX".format(d['serial']))

    print()
    print("Found {} total clients".format(len(all_clients)))
    # print(all_clients)

    print("Found {} unique clients".format(len(unique_clients)))
    # print(unique_clients)
