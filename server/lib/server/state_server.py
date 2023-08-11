import json
import os

from lib import project_path
from lib.utils.singleton import singleton_meta


@singleton_meta
class StateServer:

    @staticmethod
    def get_latest_state():
        data_file = os.path.join(project_path, 'lib/data/state.json')
        with open(data_file, 'r') as f:
            data = json.load(f)
            return data
