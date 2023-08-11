import time

from threading import Thread, Event

from lib.utils.drivers.core.fork_safe_client import ForkSafeClient, validate_client
from lib.utils.log_utils import CustomLogger


class SafeDBPool(ForkSafeClient):
    def __init__(self, host, port, user, password, dbname, mincached=0, maxcached=5, init=False, **kwargs):
        super(SafeDBPool, self).__init__(host, port, user, password, dbname)
        self._mincached = mincached
        self._maxcached = maxcached
        self.logger = kwargs.pop('logger', CustomLogger())
        self._kwargs = kwargs

        if init:
            self._pool = self.initialize()
        else:
            self._pool = None
        self.stop_event = None

    @property
    def _cls_name(self):
        return self.__class__.__name__

    @property
    def client_initialized(self):
        """
        Client initialized or not.
        """
        return self._pool is not None

    def clear_up(self):
        try:
            self._pool = self._pool.colse()
            if self.stop_event:
                self.stop_event.set()
        except:
            pass
        self._pool = None

    @validate_client
    def get_cursor(self):
        conn = self.get_conn()
        try:
            cursor = conn.cursor()
            return conn, cursor
        except Exception as e:
            raise e

    @validate_client
    def get_conn(self):
        try:
            conn = self._get_conn()
            return conn
        except Exception as e:
            raise e

    @validate_client
    def _get_conn(self):
        if not self._pool:
            self.initialize()
        return self._pool.connection()

    def _keepalive_ping(self, stop_event):
        while not stop_event.is_set():
            self.logger.info('{0} connection pool keepalive ping'.format(self._cls_name))
            try:
                self._pool._ping_idle_connection()
            except Exception as e:
                self.logger.exception(e)
                self.logger.exception("{0} connection pool ping failed!".format(self._cls_name))
            time.sleep(300)

    def spawn_ping_thread(self):
        self.logger.info('{0} connection pool spawn keep_alive ping thread'.format(self._cls_name))
        self.stop_event = Event()
        t = Thread(target=self._keepalive_ping, args=(self.stop_event, ))
        t.setDaemon(True)
        t.start()

    def get_dict_cursor(self):
        raise NotImplementedError

    def close(self):
        self.__del__()

    def __del__(self):
        self.clear_up()


__all__ = [
    'SafeDBPool'
]
