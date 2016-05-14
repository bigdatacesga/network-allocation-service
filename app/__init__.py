import os
from flask import Flask
from flask import Blueprint

app = Flask(__name__)
# Read configuration to apply from environment
config_name = os.environ.get('FLASK_CONFIG', 'development')
# apply configuration
cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
app.config.from_pyfile(cfg)

# Configure networks endpoint
from . import networks
#FIXME: Add to configuration options
networks.connect('http://10.112.0.101:8500/v1/kv')

# Create a blueprint
api = Blueprint('api', __name__)
# Import the endpoints belonging to this blueprint
from . import endpoints
from . import errors

# register blueprints
app.register_blueprint(api, url_prefix='/resources/networks/v1')
