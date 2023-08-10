import cx_Oracle as Oracle

from .core.db_utils import SubPooledDB
from .core.fork_safe_db_client import SafeDBPool

QUERY_LIMIT_NUM = 1000


class ForkSafeOraclePool(SafeDBPool):
    def __init__(self, host, port, username, password, service_name,
                 mincached=1, maxcached=5, maxconnections=5,
                 blocking=True, maxusage=None, **kwargs):
        self._maxconnections = maxconnections
        self._blocking = blocking
        self._maxusage = maxusage
        super(ForkSafeOraclePool, self).__init__(
            host, port, username, password, service_name, mincached=mincached, maxcached=maxcached, **kwargs)

    @property
    def service_name(self):
        return self._dbname

    def initialize(self):
        # makedsn 第三位默认参数是sid， 在rac集群中使用sid连接会报错，需要显式指定为service_name
        dsn = Oracle.makedsn(self._host, self._port, service_name=self.service_name)
        self._pool = SubPooledDB(
            Oracle,
            mincached=self._mincached,
            maxcached=self._maxcached,
            maxconnections=self._maxconnections,
            blocking=self._blocking,
            user=self._username,
            password=self._password,
            dsn=dsn,
            maxusage=self._maxusage,
            encoding='UTF-8',
            nencoding='UTF-8',
        )
        self.spawn_ping_thread()
        return self._pool


__all__ = [
    'ForkSafeOraclePool'
]
