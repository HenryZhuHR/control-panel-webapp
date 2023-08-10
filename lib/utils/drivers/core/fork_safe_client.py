import os
import time
import threading


def validate_client(func):
    """
    Validate client: if the client is not properly initialized, make it.

    Args:
        func(function): methods defined in class.

    Returns:
        function: validate the client in prior to execute methods.
    """
    def _validate_client(self, *args, **kwargs):
        self._check_pid()
        if not self.client_initialized:
            self.initialize()
        return func(self, *args, **kwargs)

    return _validate_client


class ForkSafeClient(object):
    """
    Fork safe client:
        1. fork lock: protect the client reset procedure.
        2. pid: record the pid of current client, if process pid != this pid, then reset the client.
    """
    def __init__(self, host, port, username, password, dbname, init=False):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._dbname = dbname

        self._fork_lock = threading.Lock()
        self._pid = os.getpid()
        if init:
            self._reset()

    @property
    def client_initialized(self):
        """
        Client initialized or not.
        """
        raise NotImplementedError

    def initialize(self):
        """
        Initialize: check if the client key in client map, reconstruct the client and db if not.
        """
        raise NotImplementedError

    def clear_up(self):
        """
        Clear up profile.
        """
        raise NotImplementedError

    def _reset(self):
        """
        Reset client:
            1. clear up client profile;
            2. initialize client profile;
            3. record current pid.
        """
        self.clear_up()
        self.initialize()
        self._pid = os.getpid()

    def _check_pid(self):
        """
        Check pid:
            if pid != pid of current process, then,
                1. acquire the fork lock;
                2. reset client profile;
                3. release the fork lock.
        """
        if self._pid != os.getpid():
            # timeout: 5 seconds.
            timeout_at = time.time() + 5
            acquired = False
            while time.time() < timeout_at:
                acquired = self._fork_lock.acquire(False)
                if acquired:
                    break
            if not acquired:
                raise Exception('child deadlock')
            try:
                if self._pid != os.getpid():
                    self._reset()
            finally:
                self._fork_lock.release()


__all__ = [
    'validate_client',
    'ForkSafeClient'
]
