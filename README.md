# meraki_api_tools

Collection of python-based Meraki API tools

* [get_clients.py](get_clients.py) = get client counts for all networks within an organization
* [create_network.py](create_network.py) = create new network, or use import file
* [get_vlans.py](get_vlans.py) = get list of vlan information from provided network
* [put_vlans.py](put_vlans.py) = take JSON input (from get_vlans.py) and modify networks

Extras:

* [utils.py](utils.py) = common functions across tools
* [create_file_template.csv](create_file_template.csv) = template for create_network import file


# TODO

* top applications for guest
* time spent on guest
* bandwidth spent on guest
* change template binding
