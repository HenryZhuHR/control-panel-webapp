import os
import threading
import time

from dbutils.pooled_db import PooledDB


class SubPooledDB(PooledDB):
    def _ping_idle_connection(self):
        """ping all connections in the pool."""
        self._lock.acquire()
        try:
            for con in self._idle_cache:  # ping all idle connections
                try:
                    con._ping_check()
                except Exception:
                    pass
            if self._maxshared:  # ping all shared connections
                for con in self._shared_cache:
                    try:
                        con.con._ping_check()
                    except Exception:
                        pass
            self._lock.notifyAll()
        finally:
            self._lock.release()


__all__ = [
    'SubPooledDB'
]
