import os
try:
    from urlparse import urlparse, parse_qs
except:
    from urllib.parse import urlparse, parse_qs
from pymongo import MongoClient
from gridfs import GridFS
from .core.fork_safe_client import ForkSafeClient, validate_client


class ForkSafeMongoClient(ForkSafeClient):
    """
    Client profile:
        1. client login messages: host, port, username, password, dbname
        2. client components:
            * client_map: cache for effective client currently, the format of key is "host:port"
            * client: effective client currently
            * db: effective db currently
    """

    _client_map = dict()

    def __init__(self, host, port=None, username=None, password=None, dbname=None, **kwargs):
        super(ForkSafeMongoClient, self).__init__(host, port, username, password, dbname)
        self._kwargs = kwargs

        self._client = None
        self._db = None

    @property
    def client_initialized(self):
        """
        Client initialized or not.
        """
        return self._client is not None

    def initialize(self):
        """
        Initialize: check if the client key in client map, reconstruct the client and db if not.
        """
        if self._host.find("mongodb://") >= 0:
            parsed = urlparse(self._host)
            client_key = parsed.netloc
            kwargs = {k: v[0] for k, v in parse_qs(parsed.query).items()}
            if kwargs:
                self._kwargs.update(kwargs)
        else:
            _host = self._host.replace('mongodb://', '')
            client_key = '%s:%s' % (_host, self._port) if self._port else _host
        if client_key not in self._client_map or self._pid != os.getpid():
            # Compatible for MongoDB 4.0+
            mongo_connect_url = "mongodb://{url}/".format(url=client_key)
            client = MongoClient(mongo_connect_url, connect=False, **self._kwargs)
            self._client_map[client_key] = client
        self._client = self._client_map[client_key]
        self._db = self._client[self._dbname]
        self._db.authenticate(name=self._username, password=self._password)

    def clear_up(self):
        """
        Clear up profile.
        """
        self._client_map.clear()
        self._client = None
        self._db = None

    @validate_client
    def get_db(self):
        """
        Get current db.

        Returns:
            pymongo.Database: a pymongo database instance.
        """
        return self._db

    @validate_client
    def get_collection(self, col_name, **kwargs):
        """
        Get a specific collection.

        Args:
            col_name(string): collection name.

        Returns:
            pymongo.Collection: a pymongo collection instance.
        """
        return self._db.get_collection(col_name, **kwargs)

    @validate_client
    def get_gridfs(self, col_name):
        """
        获取gridfsj句柄
        Args:
            col_name(str):

        Returns(GridFS):

        """
        return GridFS(self._db, col_name)

    def get_index_info(self):
        mongo_index_dict = {collection: self._db[collection].index_information()
                            for collection in self._db.collection_names()}
        return mongo_index_dict

    @validate_client
    def __getitem__(self, col_name):
        """
        Get collection by brackets as client[col_name]

        e.g. using client["example"] to get the collection named "example".

        Args:
            col_name(string): collection name.

        Returns:
            pymongo.Collection: a pymongo collection instance.
        """
        return self._db[col_name]

    @validate_client
    def __getattr__(self, item):
        """
        Overload this method for simultaneously support of two scenarios:
            * get class attributes: if item hit the class attributes name,
                return the origin attribute or function call.
                (raise error upon private attribute name that starts with '__')
            * get collections: if item doesn't hit the class attributes name,
                treat it as a collection name and return matched pymongo.Collection.

        Returns:
            pymongo.Collection: a pymongo collection instance.
        """
        return self._db[item]


__all__ = [
    'ForkSafeMongoClient'
]
