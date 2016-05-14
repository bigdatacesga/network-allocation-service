"""Networks Allocation API

    list(): show the list of networks
    show(net): show the properties of net
    register(net): register the given network
    addresses(net): show addresses of net
    addresses(net, status='free'): show only free addresses
    addresses(net, status='used'): show only free addresses
    allocate(net, address, status): add/update address
    status(net, address): show status of given network address


admin_net = {
    'name': 'admin',
    'description': 'Internal administration network using virbrPRIVATE',
    'bridge': 'virbrPRIVATE',
    'network': '10.112.0.0',
    'netmask': '16',
    'gateway': '10.112.0.1',
    'addresses': ['10.112.243.{}'.format(n) for n in range(1, 255)]
}
storage_net = {
    'name': 'storage',
    'description': 'Storage network using virbrSTORAGE',
    'bridge': 'virbrSTORAGE',
    'network': '10.117.0.0',
    'netmask': '16',
    'gateway': '',
    'addresses': ['10.117.243.{}'.format(n) for n in range(1, 255)]
}
"""
import kvstore

# Create a global kvstore client
#ENDPOINT = 'http://10.112.0.101:8500/v1/kv'
ENDPOINT = 'http://127.0.0.1:8500/v1/kv'
_kv = kvstore.Client(ENDPOINT)
PREFIX = 'resources/networks'


def connect(endpoint):
    """Set up the connection with the K/V store"""
    global _kv
    _kv = kvstore.Client(endpoint)


def register(network):
    """Register a new network

    network = {
        'name': 'admin',
        'description': 'Internal administration network using virbrPRIVATE',
        'bridge': 'virbrPRIVATE',
        'network': '10.112.0.0',
        'netmask': '16',
        'gateway': '10.112.0.1',
        'addresses': ['10.112.243.{}'.format(n) for n in range(1, 255)]
    }
    """
    basedn = '{0}/{1}'.format(PREFIX, network['name'])
    for prop in network.keys():
        if prop == 'addresses':
            for address in network[prop]:
                _kv.set('{0}/addresses/{1}'.format(basedn, address), 'free')
        else:
            _kv.set('{0}/{1}'.format(basedn, prop), network[prop])


def list():
    """Returns the list of registered networks"""
    subtree = _kv.recurse(PREFIX)
    return {'networks': [subtree[k] for k in subtree.keys() if k.endswith('/name')]}


def show(network):
    """Show the properties of a given network"""
    properties = {}
    for k in ('name', 'description', 'bridge', 'network', 'netmask', 'gateway'):
        properties[k] = _kv.get('{0}/{1}/{2}'.format(PREFIX, network, k))
    return properties


def addresses(network, status='all'):
    """Returns the status of all the addresses of a given network

    The addresses can be filtered by status using the status optional parameter
    which can take the values: 'all', 'free', 'used'
    """
    subtree = _kv.recurse('{0}/{1}/addresses'.format(PREFIX, network))
    if status == 'free':
        return filter(_parse_net_info(subtree), "free")
        #return [{"address": _parse_address(k), "status": "free"} for k in subtree.keys() if k.endswith("status") and subtree[k] == 'free']
    elif status == 'used':
        #return [{"address": _parse_address(k), "status": "used"} for k in subtree.keys() if k.endswith("status") and subtree[k] != 'free']
        return filter(_parse_net_info(subtree), "used")
    else:
        #return [{"address": _parse_address(k)} for k in subtree.keys() if k.endswith("address")]
        return _parse_net_info(subtree)


def allocate(network, address, host, clustername, node):
    """Allocate a given network address to a given host"""
    _kv.set('{0}/{1}/addresses/{2}/status'.format(PREFIX, network, address), host)
    _kv.set('{0}/{1}/addresses/{2}/clustername'.format(PREFIX, network, address), clustername)
    _kv.set('{0}/{1}/addresses/{2}/node'.format(PREFIX, network, address), node)


def deallocate(network, address):
    """Deallocate a given network address"""
    _kv.set('{0}/{1}/addresses/{2}/status'.format(PREFIX, network, address), 'free')


def status(network, address):
    """Returns the status of a given network address"""
    return _kv.get('{0}/{1}/addresses/{2}/status'.format(PREFIX, network, address))


def filter(nets, status):
    new_nets = []
    for net in nets:
        if net["status"] == status:
            new_nets.append(net)
    return new_nets

def _parse_net_info(subtree):
    nets_info = dict()

    for k in subtree.keys():
        address = _parse_address(k)
        nets_info[address] = dict()

    for k in subtree.keys():
        address = _parse_address(k)
        nets_info[address][_parse_last_element(k)] = subtree[k]

    nets_list = []

    for k in nets_info.keys():
        nets_list.append(nets_info[k])
    return nets_list

def _parse_last_element(key):
    return key.split('/')[-1]

def _parse_networkname(key):
    """Extract network name from key"""
    index = len(PREFIX.split('/'))
    return key.split('/')[index]


def _parse_address(key):
    """Extract address from key"""
    return key.split('/')[-2]
