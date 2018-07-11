import docker

ipam_pool = docker.types.IPAMPool(
            subnet='192.168.52.0/24',
            gateway='192.168.52.254'
    )
ipam_config = docker.types.IPAMConfig(
    pool_configs=[ipam_pool]
)

class WarGame(object):

    """
    게임 관리 오브젝트

    """
    def __init__(self, images=["ubuntu", "node_echo_server"], *args):
        """

        """
        self.client = docker.from_env()
        self.images = images
        self.running_containers = []
        self.network = []
        self.ipam_pool = ipam_pool
        self.ipam_config = ipam_config

    def check_for_init(self):
        if(self.client is not None):
            return True
        else:
            return False

    def run_server(self):
        """
        :return: list of containers
        """
        count = 0
        for image in self.images:
            container = self.client.containers.run(image, detach="True"
            , name="server{}".format(count)
            , domainname="server{}".format(count))
            
            self.running_containers.append(container)
            count = count + 1
        
        return self.running_containers
    def run_snort(self):
        """
        :return: snort container
        """
        container = self.client.containers.run('linton/docker-snort',
            detach="True",
            cap_add=["NET_ADMIN"])
        return container

    def stop_server(self):
        for container in self.running_containers:
            container.stop()
            container.remove()

    def get_score(self):
        pass

    def list_containers(self):
        return self.running_containers

    def create_network(self):
        """
        :return: list of network
        """
        network = self.client.networks.create(
            "wargame_network", driver="bridge",ipam=ipam_config)
        self.network.append(network)
        return self.network

    def remove_network(self):
        for network in self.network:
            network.remove()
    
    def connect_container(self, network, container):
        """
        :network: Docker.client.network
        :container: Dokcer.client.container
        """
        network.connect(container)
        network.reload()

    def get_ipam_pool(self):
        return self.ipam_pool

    def set_ipam_config(self, ipam_pool=ipam_pool):
        """
        :ipam_pool: Docker.types.IPAMPool
        """
        self.ipam_config = docker.types.IPAMConfig(
            pool_configs=[ipam_pool]
        )