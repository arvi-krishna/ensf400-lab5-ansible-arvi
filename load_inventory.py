from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager

# Initialize necessary objects
data_loader = DataLoader()
inventory_manager = InventoryManager(loader=data_loader)

# Load inventory file
inventory_path = 'hosts.yml'
inventory_manager.read_file(inventory_path)

# Print host information
print("Hosts in this inventory:")
for host in inventory_manager.get_hosts():
    print(f"Host Name: {host.get_name()}, IP Address: {host.get_vars().get('ansible_host')}, Groups: {host.get_groups()}")
