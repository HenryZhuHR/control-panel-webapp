from functools import wraps


def singleton_meta(cls):
    instances = {}

    # @synchronized
    @wraps(cls)
    def get_instance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return get_instance
