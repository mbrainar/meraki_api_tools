# meraki_api_tools

Collection of python-based Meraki API tools

## Use cases

1. Get client counts information from networks

  * [get_clients.py](get_clients.py) = get client counts for all networks within an organization

2. Batch create new networks

  * [create_network.py](create_network.py) = create new network, or use import file
  * [create_file_template.csv](create_file_template.csv) = template for create_network import file

3. Automate template change and VLAN readdressing

  * [get_vlans.py](get_vlans.py) = get list of vlan information from provided network
  * [put_vlans.py](put_vlans.py) = take JSON input (from get_vlans.py) and modify networks
  * [change_template.py](change_template.py) = unbind network from template, then bind to new template provided


Extras:

* [utils.py](utils.py) = common functions across tools


# TODO

* top applications for guest
* time spent on guest
* bandwidth spent on guest
* bulk template changes from CSV or network tag
