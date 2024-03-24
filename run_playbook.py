from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.plugins.callback import CallbackBase
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible import context

# Create a custom callback class to capture results
class ResultsCallback(CallbackBase):
    def __init__(self):
        super().__init__()
        self.hosts = []

    def v2_runner_on_ok(self, result):
        self.hosts.append({
            'name': result._host.get_name(),
            'ip': result._host.get_vars().get('ansible_host'),
            'groups': result._host.get_groups()
        })

# Initialize necessary objects
data_loader = DataLoader()
inventory_manager = InventoryManager(loader=data_loader)
variable_manager = VariableManager(loader=data_loader, inventory=inventory_manager)
callback = ResultsCallback()

# Load inventory file
inventory_path = 'hosts.yml'
inventory_manager.read_file(inventory_path)

# Set CLI arguments for the playbook execution
context.CLIARGS = {
    'verbosity': 0,
    'listhosts': None,
    'listtasks': None,
    'listtags': None,
    'syntax': None,
    'check': False,
    'diff': False,
    'inventory': inventory_path
}

# Create and execute the playbook executor
playbook_executor = PlaybookExecutor(
    playbooks=[],
    inventory=inventory_manager,
    variable_manager=variable_manager,
    loader=data_loader,
    passwords={},
)
playbook_executor._tqm._stdout_callback = callback
playbook_executor.run()

# Print the ping results
print("\nPing results:")
for host in callback.hosts:
    print(f"Host: {host['name']}, IP: {host['ip']}, Groups: {host['groups']}")
