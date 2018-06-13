# meraki_api_tools

Collection of python-based Meraki API tools

## Use cases

1. Get client counts information from networks

  * [get_clients.py](get_clients.py) = get client counts for all networks within an organization

2. Batch create new networks

  * [create_network.py](create_network.py) = create new network, or use import file
  * [create_file_template.csv](create_file_template.csv) = template for create_network import file

3. Automate template change and VLAN readdressing

  Example usage:
  ```
  export MERAKI_API_KEY=REDACTED
  python get_vlans.py -o "ACME Corp" -n "Branch 0018" -f "Branch 0018 VLANS.txt"
  python change_template.py -o "ACME Corp" -n "Branch 0018" -t "New Branch Template"
  python put_vlans.py -o "ACME Corp" -n "Branch 0018" -f "Branch 0018 VLANS.txt"
  ```

  * [get_vlans.py](get_vlans.py) = get list of vlan information from provided network
  * [change_template.py](change_template.py) = unbind network from template, then bind to new template provided
  * [put_vlans.py](put_vlans.py) = take JSON input (from get_vlans.py) and modify networks


Extras:

* [utils.py](utils.py) = common functions across tools


# TODO

* top applications for guest
* time spent on guest
* bandwidth spent on guest
* bulk template changes from CSV or network tag
