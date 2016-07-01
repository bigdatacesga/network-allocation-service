from flask import jsonify, request
from . import api
from . import networks


@api.route('/networks', methods=['GET'])
def get_networks():
    results = networks.list()
    return jsonify(results)


@api.route('/networks', methods=['POST'])
def add_network():
    # WARN: In this case we only handle Content-Type: application/json requests
    if request.get_json():
        data = request.get_json()
        if _validate_network(data):
            networks.register(data)
            return '', 204
    else:
        return jsonify({'status': '400',
                        'error': 'Invalid request',
                        'message': 'Failed to register the new '
                                   'network, invalid request'}), 400


@api.route('/networks/<network>', methods=['GET'])
def get_network_properties(network):
    results = networks.show(network)
    return jsonify(results)


@api.route('/networks/<network>/addresses', methods=['GET'])
def get_network_addresses(network):
    expanded = False
    if request.args.get('full') is not None:
        expanded = True
    if request.args.get('free') is not None:
        results = networks.addresses(network, status='free', expanded=expanded)
    elif request.args.get('used') is not None:
        results = networks.addresses(network, status='used', expanded=expanded)
    else:
        results = networks.addresses(network, status='all', expanded=expanded)
    return jsonify({"addresses": results, "number": len(results)})


@api.route('/networks/<network>/addresses/<address>', methods=['GET'])
def get_address_status(network, address):
    status = networks.status(network, address)
    return jsonify(status)


@api.route('/networks/<network>', methods=['POST'])
def allocate_addresses(network):
    """Allocate a new network address"""
    # Handle Content-Type: application/json requests
    if request.get_json():
        data = request.get_json()
        cluster = data['cluster']
        node = data['node']
    # Handle form param requests: eg. curl -d status=free
    else:
        cluster = request.form.get('cluster')
        node = request.form.get('node')

    free_addresses = networks.addresses(network, status='free', expanded=False)
    address = free_addresses[0]
    networks.allocate(network, address, node, cluster)
    return jsonify({'address': address}), 200


@api.route('/networks/<network>/addresses/<address>', methods=['PUT'])
def update_address_status(network, address):
    # Handle Content-Type: application/json requests
    if request.get_json():
        data = request.get_json()
        status = data['status']
        cluster = data['cluster']
        node = data['node']
    # Handle form param requests: eg. curl -d status=free
    else:
        status = request.form.get('status')
        cluster = request.form.get('cluster')
        node = request.form.get('node')
    if status is not None:
        if status == 'free':
            networks.deallocate(network, address)
        else:
            networks.allocate(network, address, node, cluster)
        return '', 204
    else:
        return jsonify({'status': '400',
                        'error': 'Invalid request',
                        'message': 'Unable to get the new '
                                   'address status from the request'}), 400


def _validate_network(network):
    """Validate network data"""
    required_fields = ('name', 'description', 'bridge', 'network', 'netmask',
                       'gateway', 'addresses')
    if all(field in network for field in required_fields):
        if isinstance(network['addresses'], list):
            return True
    return False


