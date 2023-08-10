import json
from functools import wraps

from flask import make_response, request

from lib.utils.log_utils import get_logger

logger = get_logger(__name__)


def cross_site(func):
    """
    cross site.
    """

    @wraps(func)
    def decorator(*args, **kwargs):
        """
        decorator
        """
        try:
            data = func(*args, **kwargs)
            code = 200
            ret = json.dumps({'code': code, 'data': data, 'msg': None}, ensure_ascii=False)
        except Exception:
            import traceback
            logger.error(traceback.format_exc())
            code = 500
            ret = json.dumps({'code': code, 'data': None, 'msg': traceback.format_exc()}, ensure_ascii=False)
        finally:
            response = make_response(ret, code)

        response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin')
        response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE,OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = \
            'Origin, X-Requested-With, Content-Type, Accept, Authorization'
        response.headers['Content-Type'] = 'application/json'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    return decorator
