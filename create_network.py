import requests
from argparse import ArgumentParser
from utils import get_org_id

def create_network(api_key, organization_id, name, type):
    url = "https://api.meraki.com/api/v0/organizations/{}/networks".format(organization_id)
    payload = "{\"name\":\""+name+"\", \"type\":\""+type+"\"}"
    headers = {
        'x-cisco-meraki-api-key': api_key,
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
        'Postman-Token': "eed11869-b5d4-477d-bcad-b93885f7dba8"
        }
    response = requests.request("POST", url, data=payload, headers=headers)

    return response.status_code, response.json()



if __name__ == '__main__':

    parser = ArgumentParser(description='Usage:')
    # script arguments
    parser.add_argument('-k', '--key', type=str, required=True,
                        help="API Key from Meraki Dashboard")
    parser.add_argument('-o', '--organization', type=str, required=True,
                        help="Name of Organization in Meraki Dashboard")
    parser.add_argument('-f', '--file', type=str, required=False,
                        help="Use file to create bulk networks")
    parser.add_argument('-n', '--name', type=str, required=False,
                        help="Name of new network")
    parser.add_argument('-t', '--type', type=str, required=False,
                        help="Type of new network. Valid types are \'wireless\', \'switch\', \'appliance\', or a space-separated list of those for a combined network.")
    args = parser.parse_args()

    api_key = args.key
    organization_name = args.organization
    # Require either -f OR (-n AND -t)
    if not args.file and (not args.name or not args.type):
        print("ERROR: Must supply either file or name and type")
        exit()
    file = args.file
    name = args.name
    type = args.type
    valid_types = ["wireless", "switch", "appliance"]
    if type and type.lower() not in valid_types:
        print("ERROR: Type must be \'wireless\', \'switch\', or \'appliance\'")
        exit()

    organization_id = get_org_id(api_key, organization_name)

    if organization_id:

        # If file provided, use that
        if file:
            count = 0
            print("Reading input from file: {}".format(file))
            fh = open(file,"r")
            for line in fh:
                fields = line.split(",")
                name = fields[0]
                type = fields[1]
                if name != "Network Name":
                    count += 1
                    api_status, network = create_network(api_key, organization_id, name, type.lower().strip())
                    if api_status == 201:
                        print("{} network \"{}\" was successfully created; network id = {}".format(network['type'], network['name'], network['id']))
                    elif api_status == 400:
                        print("Unable to create network \"{}\". Error message: {}".format(name, network['errors']))
                        break
            fh.close()

            if count == 0:
                print("No entries found in file")

        else:
            api_status, network = create_network(api_key, organization_id, name, type.lower())
            if api_status == 201:
                print("{} network \"{}\" was successfully created; network id = {}".format(network['type'], network['name'], network['id']))
            elif api_status == 400:
                print("Unable to create network. Error message: {}".format(network['errors']))
                exit()

    else:
        print("Unable to find organization: {}".format(organization_name))
        print("Check organization name, ensure you have access to organization, check API key")
        exit()
