from flask import Flask
from flask_restful import Api

from lib.models.state import StateResource

app = Flask(__name__)
api = Api(app)

api.add_resource(StateResource, '/state')
