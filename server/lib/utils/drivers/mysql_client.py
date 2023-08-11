import os
import time
from threading import Thread

import pymysql

from lib.utils.drivers.core.db_utils import SubPooledDB
from lib.utils.drivers.core.fork_safe_client import ForkSafeClient, validate_client
from lib.utils.drivers.core.fork_safe_db_client import SafeDBPool


class ForkSafeMysqlPool(SafeDBPool):
    """
    clien profile
    """
    def __init__(self, host, port, username, password, dbname, mincached=1, maxcached=5, **kwargs):
        super(ForkSafeMysqlPool, self).__init__(
            host, port, username, password, dbname, mincached=mincached, maxcached=maxcached, **kwargs)

    def initialize(self):
        self._pool = SubPooledDB(
            pymysql,
            host=self._host,
            port=self._port,
            user=self._username,
            passwd=self._password,
            db=self._dbname,
            **self._kwargs
        )
        self.spawn_ping_thread()
        return self._pool

    def get_dict_cursor(self):
        conn = self.get_conn()
        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            return conn, cursor
        except Exception as e:
            raise e


__all__ = [
    'ForkSafeMysqlPool'
]
