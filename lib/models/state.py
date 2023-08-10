from flask import request

from lib.models.base import BaseResource
from lib.server.state_server import StateServer
from lib.utils.flask_utils import cross_site


class StateResource(BaseResource):
    service = StateServer()

    @cross_site
    def get(self):
        req_data = dict(request.args)
        res = self.service.get_latest_state()
        return res

    @cross_site
    def post(self):
        pass
