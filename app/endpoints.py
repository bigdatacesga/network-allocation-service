from flask import jsonify, request
from . import api
from . import networks
from .decorators import restricted


@api.route('/networks/', methods=['GET'])
@api.route('/networks', methods=['GET'])
def get_networks():
    results = networks.list()
    return jsonify(results)


@api.route('/networks/', methods=['POST'])
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


@api.route('/networks/<network>/', methods=['GET'])
@api.route('/networks/<network>', methods=['GET'])
def get_network_properties(network):
    results = networks.show(network)
    return jsonify(results)


def _validate_network(network):
    """Validate network data"""
    required_fields = ('name', 'description', 'bridge', 'network', 'netmask',
                       'gateway', 'addresses')
    if all(field in network for field in required_fields):
        if isinstance(network['addresses'], list):
            return True
    return False


@api.route('/networks/<network>/addresses/', methods=['GET'])
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


@api.route('/networks/<network>/addresses/<address>', methods=['PUT'])
def update_address_status(network, address):
    # Handle Content-Type: application/json requests
    if request.get_json():
        data = request.get_json()
        status = data['status']
        clustername = data['clustername']
        node = data['node']
    # Handle form param requests: eg. curl -d status=free
    else:
        status = request.form.get('status')
        clustername = request.form.get('clustername')
        node = request.form.get('node')
    if status is not None:
        if status == 'free':
            networks.deallocate(network, address)
        else:
            networks.allocate(network, address, node, clustername)
        return '', 204
    else:
        return jsonify({'status': '400',
                        'error': 'Invalid request',
                        'message': 'Unable to get the new '
                                   'address status from the request'}), 400


@api.route('/test', methods=['GET'])
@restricted(role='ROLE_USER')
def echo_hello():
    return jsonify({'message': 'Hello'})
