from flask import request
from flask_restful import Resource

from lib.utils.flask_utils import cross_site


class BaseResource(Resource):

    @cross_site
    def get(self):
        raise NotImplementedError

    @cross_site
    def post(self):
        raise NotImplementedError
