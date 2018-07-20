Network Resource Allocation REST API
====================================

Purpose
-------
The objective of this module is to provide a REST API to perform
Resource Allocation of network addresses

REST API
--------
Endpoint: http://networks:5000/v1/

::
    GET networks
    {
        "admin": "Internal administration network using virbrPRIVATE",
        "storage": "Internal storage network with jumbo frames using virbrSTORAGE",
        "gluster": "Network dedicated to gluster",
        "public": "Public network",
    }

    POST networks
    {
        "name": "admin",
        "description": "Internal administration network using virbrPRIVATE",
        "bridge": "virbrPRIVATE",
        "network": "10.112.0.0",
        "netmask": "16",
        "gateway": "10.112.0.1",
        "addresses": ["10.112.1.101", "10.112.1.102", "10.112.1.103"]
    }

    GET networks/<network>
    {
        "name": "admin",
        "description": "Internal administration network using virbrPRIVATE",
        "bridge": "virbrPRIVATE",
        "network": "10.112.0.0",
        "netmask": "16",
        "gateway": "10.112.0.1",
    }

    GET networks/<network>/addresses
    {
        "addresses": ["10.112.1.101", "10.112.1.102", "10.112.1.103"]
    }

    GET networks/<network>/addresses?free
    {
        "addresses": ["10.112.1.101", "10.112.1.103"]
    }

    GET networks/<network>/addresses?used
    {
        "addresses": ["10.112.1.102"]
    }


    # Network address allocation: Atomic operation
    POST networks/<network>
    {
        "cluster": "gluster-3.7.11-8",
        "node": "glusternode0"
    }

    returns:

        {"address": "10.112.243.109"}

    # Network address allocation: manual mode (not recommended)
    PUT networks/<network>/addresses/<address>
    {
        "cluster": "gluster-3.7.11-8",
        "node": "glusternode0",
        "status": "used"
    }

    PUT networks/<network>/addresses/<address>
    {
        "cluster": "_",
        "node": "_",
        "status": "free"
    }

    GET networks/<network>/addresses?full
    {
        "addresses": [
            {
                "address": "10.117.243.104",
                "clustername": "jenes-mpi-1.7.0-1",
                "node": "node_1",
                "status": "used"
            },
            {
                "address": "10.117.243.105",
                "clustername": "jenes-mpi-1.7.0-1",
                "node": "node_0",
                "status": "used"
            }
        ],
        "number": 2
    }

    GET networks/<network>/addresses?used&full
    {
        "addresses": [
            {
                "address": "10.117.243.104",
                "clustername": "jenes-mpi-1.7.0-1",
                "node": "node_1",
                "status": "used"
            },
            {
                "address": "10.117.243.105",
                "clustername": "jenes-mpi-1.7.0-1",
                "node": "node_0",
                "status": "used"
            }
        ],
        "number": 2
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

Building a docker image
-----------------------
```
docker build -t network-allocation-service:0.1.1 .
docker tag ae2476dfecab docker-registry.cesga.es:5000/network-allocation-service:0.1.1
docker push docker-registry.cesga.es:5000/network-allocation-service:0.1.1

```

Running the service
-------------------
```
docker-executor run instances/sistemas/networks/0.1.0/1/nodes/networks1
docker-executor run instances/sistemas/networks/0.1.0/1/nodes/networks2
```

Registering networks
--------------------
```
from app import networks

net = {
        'name': 'admin',
        'description': 'Internal administration network using virbrPRIVATE',
        'bridge': 'virbrPRIVATE',
        'network': '10.112.0.0',
        'netmask': '16',
        'gateway': '10.112.0.1',
        'addresses': ['10.112.243.{}'.format(n) for n in range(1, 255)]
}

networks.register(net)

net = {
        'name': 'storage',
        'description': 'Internal storage network using virbrSTORAGE',
        'bridge': 'virbrSTORAGE',
        'network': '10.117.0.0',
        'netmask': '16',
        'gateway': '10.117.0.1',
        'addresses': ['10.117.243.{}'.format(n) for n in range(1, 255)]
}

networks.register(net)

net =  {
        'name': 'bigdata',
        'description': 'Bigdata new network using virbrBIGDATA',
        'bridge': 'virbrBIGDATA',
        'network': '10.121.0.0',
        'netmask': '16',
        'gateway': '10.121.0.1',
        'addresses': ['10.121.243.{}'.format(n) for n in range(1, 255)]
}

networks.register(net)


# To delete it
kv.delete('resources/networks/admin', recursive=True)

```

