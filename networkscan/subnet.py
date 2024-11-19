import ipaddress

class subnet():
    def __init__(self,subnet,cidr):
        self.subnet = subnet
        self.cidr = cidr

    def get_all_possible_hosts(self):
        network = ipaddress.ip_network(f'{self.subnet}/{self.cidr}')
        return list(network.hosts())



        