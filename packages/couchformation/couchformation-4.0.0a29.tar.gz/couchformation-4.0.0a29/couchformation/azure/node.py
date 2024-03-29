##
##

import re
import logging
from itertools import cycle, islice
from couchformation.azure.driver.base import CloudBase
from couchformation.azure.driver.network import Network
from couchformation.azure.driver.instance import Instance
from couchformation.azure.driver.machine import MachineType
from couchformation.azure.driver.disk import Disk
from couchformation.azure.driver.image import Image
from couchformation.azure.driver.dns import DNS
from couchformation.azure.driver.private_dns import PrivateDNS
from couchformation.azure.network import AzureNetwork
from couchformation.config import get_state_file, get_state_dir
from couchformation.ssh import SSHUtil
from couchformation.exception import FatalError
from couchformation.kvdb import KeyValueStore
from couchformation.util import FileManager, Synchronize
import couchformation.constants as C
from couchformation.util import PasswordUtility

logger = logging.getLogger('couchformation.azure.node')
logger.addHandler(logging.NullHandler())


class AzureNodeError(FatalError):
    pass


class AzureDeployment(object):

    def __init__(self, parameters: dict):
        self.parameters = parameters
        self.name = parameters.get('name')
        self.project = parameters.get('project')
        self.region = parameters.get('region')
        self.zone = parameters.get('zone')
        self.auth_mode = parameters.get('auth_mode')
        self.profile = parameters.get('profile')
        self.ssh_key = parameters.get('ssh_key')
        self.os_id = parameters.get('os_id')
        self.os_version = parameters.get('os_version')
        self.feature = parameters.get('feature')
        self.cloud = parameters.get('cloud')
        self.number = parameters.get('number')
        self.machine_type = parameters.get('machine_type')
        self.password = parameters.get('password') if parameters.get('password') else PasswordUtility().generate(16)
        self.volume_size = parameters.get('volume_size') if parameters.get('volume_size') else "256"
        self.services = parameters.get('services') if parameters.get('services') else "default"
        self.node_name = f"{self.name}-node-{self.number:02d}"
        self.boot_disk = f"{self.name}-boot-{self.number:02d}"
        self.swap_disk = f"{self.name}-swap-{self.number:02d}"
        self.data_disk = f"{self.name}-data-{self.number:02d}"
        self.node_pub_ip = f"{self.name}-node-{self.number:02d}-pub-ip"
        self.node_nic = f"{self.name}-node-{self.number:02d}-nic"

        filename = get_state_file(self.project, self.name)

        with Synchronize(C.GLOBAL_LOCK):
            try:
                state_dir = get_state_dir(self.project, self.name)
                FileManager().make_dir(state_dir)
            except Exception as err:
                raise AzureNodeError(f"can not create state dir: {err}")

        document = self.node_name
        self.state = KeyValueStore(filename, document)

        self.az_network = AzureNetwork(self.parameters)
        self.az_base = CloudBase(self.parameters)

    def check_state(self):
        if self.state.get('resource_group'):
            rg_name = self.state.get('resource_group')
        else:
            rg_name = f"{self.project}-rg"

        if self.state.get('instance_id'):
            result = Instance(self.parameters).details(self.state['instance_id'], rg_name)
            if result is None:
                logger.warning(f"Removing stale state entry for instance {self.state['instance_id']}")
                del self.state['instance_id']
        if self.state.get('node_nic'):
            result = Network(self.parameters).describe_nic(self.state['node_nic'], rg_name)
            if result is None:
                logger.warning(f"Removing stale state entry for NIC {self.state['node_nic']}")
                del self.state['node_nic']
        if self.state.get('node_pub_ip'):
            result = Network(self.parameters).describe_pub_ip(self.state['node_pub_ip'], rg_name)
            if result is None:
                logger.warning(f"Removing stale state entry for public IP {self.state['node_pub_ip']}")
                del self.state['node_pub_ip']
        if self.state.get('swap_disk'):
            result = Disk(self.parameters).details(self.state['swap_disk'], rg_name)
            if result is None:
                logger.warning(f"Removing stale state entry for disk {self.state['swap_disk']}")
                del self.state['swap_disk']
        if self.state.get('data_disk'):
            result = Disk(self.parameters).details(self.state['data_disk'], rg_name)
            if result is None:
                logger.warning(f"Removing stale state entry for disk {self.state['data_disk']}")
                del self.state['data_disk']
        if self.state.get('boot_disk'):
            result = Disk(self.parameters).details(self.state['boot_disk'], rg_name)
            if result is None:
                logger.warning(f"Removing stale state entry for disk {self.state['boot_disk']}")
                del self.state['boot_disk']

    def deploy(self):
        self.check_state()
        subnet_list = []

        if self.state.get('instance_id'):
            logger.info(f"Node {self.node_name} already exists")
            return self.state.as_dict

        ssh_pub_key_text = SSHUtil().get_ssh_public_key(self.ssh_key)
        rg_name = self.az_network.resource_group
        azure_location = self.az_base.region

        for n, zone_state in enumerate(self.az_network.zones):
            subnet_list.append(dict(
                subnet_id=zone_state[2],
                zone=zone_state[0],
                subnet=zone_state[1],
            ))

        if len(subnet_list) == 0:
            raise AzureNodeError(f"can not get subnet list, check project settings")

        if not self.zone:
            subnet_cycle = cycle(subnet_list)
            subnet = next(islice(subnet_cycle, self.number - 1, None))
        else:
            subnet = next((z for z in subnet_list if z['zone'] == self.zone), None)

        if not subnet:
            raise AzureNodeError(f"Can not determine availability zone (check project settings)")

        image = Image(self.parameters).list_standard(os_id=self.os_id, os_version=self.os_version)
        if not image:
            raise AzureNodeError(f"can not find image for type {self.os_id} {self.os_version}")

        logger.info(f"Using image {image['publisher']}/{image['offer']}/{image['sku']} type {image['os_id']} version {image['os_version']}")

        self.state['service'] = self.name
        self.state['username'] = image['os_user']

        machine_type = self.machine_type
        volume_size = self.volume_size
        services = self.services

        if self.feature == "vmp":
            logger.info(f"Enabling nested virtualization")
            virtualization = True
        else:
            virtualization = False

        machine = MachineType(self.parameters).get_machine(self.machine_type, azure_location, virtualization)
        if not machine:
            raise AzureNodeError(f"can not find machine for type {machine_type}")
        machine_name = machine['name']
        machine_ram = int(machine['memory'] / 1024)
        logger.info(f"Selecting machine type {machine_name}")

        swap_tier = self.az_base.disk_size_to_tier(machine_ram)
        disk_tier = self.az_base.disk_size_to_tier(volume_size)

        logger.info(f"Creating disk {self.swap_disk}")
        swap_resource = Disk(self.parameters).create(rg_name, azure_location, subnet['zone'], swap_tier['disk_size'], swap_tier['disk_tier'], self.swap_disk)
        self.state['swap_disk'] = self.swap_disk

        logger.info(f"Creating disk {self.data_disk}")
        data_resource = Disk(self.parameters).create(rg_name, azure_location, subnet['zone'], disk_tier['disk_size'], disk_tier['disk_tier'], self.data_disk)
        self.state['data_disk'] = self.data_disk

        logger.info(f"Creating public IP {self.node_pub_ip}")
        pub_ip_resource = Network(self.parameters).create_pub_ip(self.node_pub_ip, rg_name)
        self.state['node_pub_ip'] = self.node_pub_ip

        logger.info(f"Creating NIC {self.node_nic}")
        nic_resource = Network(self.parameters).create_nic(self.node_nic, subnet['subnet_id'], subnet['zone'], pub_ip_resource.id, rg_name)
        self.state['node_nic'] = self.node_nic

        logger.info(f"Creating node {self.node_name}")
        Instance(self.parameters).run(self.node_name,
                                      image['publisher'],
                                      image['offer'],
                                      image['sku'],
                                      subnet['zone'],
                                      nic_resource.id,
                                      image['os_user'],
                                      ssh_pub_key_text,
                                      rg_name,
                                      self.boot_disk,
                                      machine_type=machine_name,
                                      password=self.password)

        logger.info(f"Attaching disk {self.swap_disk}")
        Instance(self.parameters).attach_disk(self.node_name, self.az_base.disk_caching(swap_tier['disk_size']), "1", swap_resource.id, rg_name)
        logger.info(f"Attaching disk {self.data_disk}")
        Instance(self.parameters).attach_disk(self.node_name, self.az_base.disk_caching(disk_tier['disk_size']), "2", data_resource.id, rg_name)

        self.state['instance_id'] = self.node_name
        self.state['name'] = self.node_name
        self.state['services'] = services
        self.state['zone'] = subnet['zone']
        self.state['resource_group'] = rg_name
        self.state['boot_disk'] = self.boot_disk
        self.az_network.add_service(self.node_name)

        nic_details = Network(self.parameters).describe_nic(self.node_nic, rg_name)
        pub_ip_details = Network(self.parameters).describe_pub_ip(self.node_pub_ip, rg_name)
        self.state['public_ip'] = pub_ip_details.ip_address
        self.state['private_ip'] = nic_details.ip_configurations[0].private_ip_address

        if self.az_network.public_zone and self.az_network.domain_name and not self.state.get('public_hostname'):
            host_name = f"{self.node_name}.{self.az_network.domain_name}"
            DNS(self.parameters).add_record(self.az_network.public_zone, host_name, [self.state['public_ip']], rg_name)
            self.state['public_zone_id'] = self.az_network.public_zone
            self.state['public_hostname'] = host_name

        if self.az_network.private_zone and self.az_network.domain_name and not self.state.get('private_hostname'):
            host_name = f"{self.node_name}.{self.az_network.domain_name}"
            PrivateDNS(self.parameters).add_record(self.az_network.private_zone, host_name, [self.state['private_ip']], rg_name)
            self.state['private_zone_id'] = self.az_network.private_zone
            self.state['private_hostname'] = host_name

        if image['os_id'] == 'windows':
            self.state['host_password'] = self.password

        logger.info(f"Created instance {self.node_name}")
        return self.state.as_dict

    def destroy(self):
        rg_name = self.state['resource_group']
        if self.state.get('public_hostname'):
            domain_id = self.state['public_zone_id']
            name = self.state['public_hostname']
            ip = self.state['public_ip']
            DNS(self.parameters).delete_record(domain_id, name, rg_name)
            logger.info(f"Deleted DNS record for {ip}")
        if self.state.get('private_hostname'):
            domain_id = self.state['private_zone_id']
            name = self.state['private_hostname']
            ip = self.state['private_ip']
            PrivateDNS(self.parameters).delete_record(domain_id, name, rg_name)
            logger.info(f"Deleted DNS record for {ip}")
        if self.state.get('instance_id'):
            instance_name = self.state['instance_id']
            node_nic = self.state['node_nic']
            node_pub_ip = self.state['node_pub_ip']
            Instance(self.parameters).terminate(instance_name, rg_name)
            logger.info(f"Removed instance {instance_name}")
            Network(self.parameters).delete_nic(node_nic, rg_name)
            logger.info(f"Removed NIC {node_nic}")
            Network(self.parameters).delete_pub_ip(node_pub_ip, rg_name)
            logger.info(f"Removed public IP {node_pub_ip}")
            Disk(self.parameters).delete(self.state['swap_disk'], rg_name)
            logger.info(f"Removed disk {self.state['swap_disk']}")
            Disk(self.parameters).delete(self.state['data_disk'], rg_name)
            logger.info(f"Removed disk {self.state['data_disk']}")
            Disk(self.parameters).delete(self.state['boot_disk'], rg_name)
            logger.info(f"Removed disk {self.state['boot_disk']}")
            self.state.clear()
            self.az_network.remove_service(self.node_name)
            logger.info(f"Removed instance {instance_name}")

    def info(self):
        return self.state.as_dict

    @staticmethod
    def _name_check(value):
        p = re.compile(r"^[a-z]([-_a-z0-9]*[a-z0-9])?$")
        if p.match(value):
            return value
        else:
            raise AzureNodeError("names must only contain letters, numbers, dashes and underscores")
