Network Resource Allocation REST API
====================================

Purpose
-------
The objective of this module is to provide a REST API to perform
Resource Allocation of network addresses

REST API
--------
Endpoint: resources/networks/v1

::
    GET networks
    {
        'admin': 'Internal administration network using virbrPRIVATE',
        'storage': 'Internal storage network with jumbo frames using virbrSTORAGE',
        'gluster': 'Network dedicated to gluster',
        'public': 'Public network',
    }

    POST networks
    {
        'name': 'admin',
        'description': 'Internal administration network using virbrPRIVATE',
        'bridge': 'virbrPRIVATE',
        'network': '10.112.0.0',
        'netmask': '16',
        'gateway': '10.112.0.1',
        'addresses': ['10.112.1.101', '10.112.1.102', '10.112.1.103']
    }

    GET networks/<network>
    {
        'name': 'admin',
        'description': 'Internal administration network using virbrPRIVATE',
        'bridge': 'virbrPRIVATE',
        'network': '10.112.0.0',
        'netmask': '16',
        'gateway': '10.112.0.1',
    }

    GET networks/<network>/addresses
    {
        'addresses': ['10.112.1.101', '10.112.1.102', '10.112.1.103']
    }

    GET networks/<network>/addresses?free
    {
        'addresses': ['10.112.1.101', '10.112.1.103']
    }

    GET networks/<network>/addresses?used
    {
        'addresses': ['10.112.1.102']
    }

    PUT networks/<network>/addresses/<address>
    {
        'status': 'docker-jlopez-flexlm-1'
    }

KV Store
--------
/resources/<network>/<address>/status

Deployment
----------

Installation::

    virtualenv venv
    . venv/bin/activate
    pip install -r requirements.txt
    pip install gunicorn

Running the application in production using screen::

    su - restuser
    cd <install_dir>
    . venv/bin/activate
    FLASK_CONFIG=production gunicorn --workers=2 --bind=:5000 wsgi:application

Registry information:

nodes = {
  'networks1': {'cpu': '1',
               'disks': {},
               'host': '',
               'id': '',
               'mem': '1024',
               'name': 'networks1',
               'networks': {'eth0': {'address': '10.112.0.104',
                                     'bridge': 'virbrPRIVATE',
                                     'gateway': '10.112.0.1',
                                     'netmask': '16',
                                     'network': '10.112.0.0'}},
               'services': ['networks'],
               'status': 'pending'},
 'networks2': {'cpu': '1',
               'disks': {},
               'host': '',
               'id': '',
               'mem': '1024',
               'name': 'networks2',
               'networks': {'eth0': {'address': '10.112.0.105',
                                     'bridge': 'virbrPRIVATE',
                                     'gateway': '10.112.0.1',
                                     'netmask': '16',
                                     'network': '10.112.0.0'}},
               'services': ['networks'],
               'status': 'pending'}
}

services = {}

kv.delete('instances/sistemas/networks/0.1.0/1', recursive=True)
registry.register(user='sistemas', framework='networks', flavour='0.1.0', nodes=nodes, services={'networks': {}})
kv.set('instances/sistemas/networks/0.1.0/1/nodes/networks1/networks/eth0/address', '10.112.0.104')
kv.set('instances/sistemas/networks/0.1.0/1/nodes/networks1/networks/eth0/bridge', 'virbrPRIVATE')
kv.set('instances/sistemas/networks/0.1.0/1/nodes/networks1/networks/eth0/gateway', '10.112.0.1')
kv.set('instances/sistemas/networks/0.1.0/1/nodes/networks1/networks/eth0/netmask', '16')
kv.set('instances/sistemas/networks/0.1.0/1/nodes/networks1/networks/eth0/network', '10.112.0.1')
kv.set('instances/sistemas/networks/0.1.0/1/nodes/networks1/clustername', 'rest')
kv.set('instances/sistemas/networks/0.1.0/1/nodes/networks1/docker_image', 'docker-registry.cesga.es:5000/network-allocation-service:0.1.0')
kv.set('instances/sistemas/networks/0.1.0/1/nodes/networks1/docker_opts', '')


kv.set('instances/sistemas/networks/0.1.0/1/nodes/networks2/networks/eth0/address', '10.112.0.105')
kv.set('instances/sistemas/networks/0.1.0/1/nodes/networks2/networks/eth0/bridge', 'virbrPRIVATE')
kv.set('instances/sistemas/networks/0.1.0/1/nodes/networks2/networks/eth0/gateway', '10.112.0.1')
kv.set('instances/sistemas/networks/0.1.0/1/nodes/networks2/networks/eth0/netmask', '16')
kv.set('instances/sistemas/networks/0.1.0/1/nodes/networks2/networks/eth0/network', '10.112.0.1')

