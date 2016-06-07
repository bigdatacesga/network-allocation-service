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
    'networkname': 'admin',
    'description': 'Internal administration network using virbrPRIVATE',
    'bridge': 'virbrPRIVATE',
    'network': '10.112.0.0',
    'netmask': '16',
    'gateway': '10.112.0.1',
    'addresses': ['10.112.243.{}'.format(n) for n in range(1, 255)]
}
storage_net = {
    'networkname': 'storage',
    'description': 'Storage network using virbrSTORAGE',
    'bridge': 'virbrSTORAGE',
    'network': '10.117.0.0',
    'netmask': '16',
    'gateway': '',
    'addresses': ['10.117.243.{}'.format(n) for n in range(1, 255)]
}
"""
import kvstore

NETWORKS_VERSION_PATH = "production"

# Create a global kvstore client
ENDPOINT = 'http://10.112.0.101:8500/v1/kv'

_kv = kvstore.Client(ENDPOINT)
PREFIX = 'resources/networks/' + NETWORKS_VERSION_PATH


def connect(endpoint):
    """Set up the connection with the K/V store"""
    global _kv
    _kv = kvstore.Client(endpoint)


def register(network):
    """Register a new network

    network = {
        'networkname': 'admin',
        'description': 'Internal administration network using virbrPRIVATE',
        'bridge': 'virbrPRIVATE',
        'network': '10.112.0.0',
        'netmask': '16',
        'gateway': '10.112.0.1',
        'addresses': ['10.112.243.{}'.format(n) for n in range(1, 255)]
    }
    """
    basedn = '{0}/{1}'.format(PREFIX, network['networkname'])
    for prop in network.keys():
        if prop == 'addresses':
            for address in network[prop]:
                _kv.set('{0}/addresses/{1}/status'.format(basedn, address), 'free')
                _kv.set('{0}/addresses/{1}/address'.format(basedn, address), address)
                _kv.set('{0}/addresses/{1}/clustername'.format(basedn, address), '_')
                _kv.set('{0}/addresses/{1}/node'.format(basedn, address), '_')
        else:
            _kv.set('{0}/{1}'.format(basedn, prop), network[prop])


def list():
    """Returns the list of registered networks"""
    subtree = _kv.recurse(PREFIX)
    return {'networks': [subtree[k] for k in subtree.keys() if k.endswith('/networkname')]}


def show(network):
    """Show the properties of a given network"""
    properties = {}
    for k in ('description', 'bridge', 'network', 'netmask', 'gateway', 'networkname'):
        properties[k] = _kv.get('{0}/{1}/{2}'.format(PREFIX, network, k))
    return properties


def addresses(network, status='all', expanded=False):
    """Returns the status of all the addresses of a given network

    The addresses can be filtered by status using the status optional parameter
    which can take the values: 'all', 'free', 'used'
    """
    subtree = _kv.recurse('{0}/{1}/addresses'.format(PREFIX, network))
    if status == 'free' or status == 'used':
        addresses = _filter(_parse_net_info(subtree), status)
    else:
        addresses = _parse_net_info(subtree)
    return _format(addresses, expanded)


def _format(addresses, expanded=False):
    """Adjust output format of the addresses depending on the verbosity requested
    
    expanded=True means all the details about each address are given
    expanded=False means only the list of IP addresses is returned
    """
    if expanded:
        return addresses
    else:
        return [ip['address'] for ip in addresses]


def allocate(network, address, node, cluster='_'):
    """Allocate a given network address to a given node that can belong to a cluster"""
    _kv.set('{0}/{1}/addresses/{2}/status'.format(PREFIX, network, address), 'used')
    _kv.set('{0}/{1}/addresses/{2}/cluster'.format(PREFIX, network, address), cluster)
    _kv.set('{0}/{1}/addresses/{2}/node'.format(PREFIX, network, address), node)


def deallocate(network, address):
    """Deallocate a given network address"""
    _kv.set('{0}/{1}/addresses/{2}/status'.format(PREFIX, network, address), 'free')
    _kv.set('{0}/{1}/addresses/{2}/cluster'.format(PREFIX, network, address), '_')
    _kv.set('{0}/{1}/addresses/{2}/node'.format(PREFIX, network, address), '_')


def status(network, address):
    """Returns the status of a given network address"""
    status = {}
    status['status'] = _kv.get(
        '{0}/{1}/addresses/{2}/status'.format(PREFIX, network, address))
    status['clustername'] = _kv.get(
        '{0}/{1}/addresses/{2}/clustername'.format(PREFIX, network, address)) 
    status['node'] = _kv.get('{0}/{1}/addresses/{2}/node'.format(PREFIX, network, address))
    return status


def _filter(addresses, status):
    """Filter addresses by status"""
    return [ip for ip in addresses if ip["status"] == status]


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
