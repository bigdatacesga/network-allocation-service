from flask import jsonify, request
from . import api
from . import networks
from .decorators import restricted


@api.route('/networks/', methods=['GET'])
@api.route('/networks', methods=['GET'])
def get_networks():
    results = networks.list()
    return jsonify(results)


@api.route('/networks/<network>/', methods=['GET'])
@api.route('/networks/<network>', methods=['GET'])
def get_network_properties(network):
    results = networks.show(network)
    return jsonify(results)


@api.route('/networks/<network>/addresses/', methods=['GET'])
@api.route('/networks/<network>/addresses', methods=['GET'])
def get_network_addresses(network):
    if request.args.get('free') is not None:
        results = networks.addresses(network, status='free')
    elif request.args.get('used') is not None:
        results = networks.addresses(network, status='used')
    else:
        results = networks.addresses(network)
    return jsonify({"addresses": results, "number": len(results)})


@api.route('/networks/<network>/addresses/<address>', methods=['GET'])
def get_address_status(network, address):
    status = networks.status(network, address)
    return jsonify({'status': status})


@api.route('/networks/<network>/addresses/<address>', methods=['PUT'])
def update_address_status(network, address):
    # Handle Content-Type: application/json requests
    if request.get_json():
        data = request.get_json()
        address_status = data['status']
        address_clustername = data['clustername']
        address_node = data['node']
    # Handle form param requests: eg. curl -d status=free
    else:
        address_status = request.form.get('status')
        address_clustername = request.form.get('clustername')
        address_node = request.form.get('node')
    if address_status is not None:
        if address_status == 'free':
            networks.deallocate(network, address)
        else:
            # TODO strange behaviour, state is passed but 'host' is expected, see allocate function
            networks.allocate(network, address, address_status, address_clustername, address_node)
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
