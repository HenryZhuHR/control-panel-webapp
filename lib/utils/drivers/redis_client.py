import rediscluster
import redis
from redis.sentinel import Sentinel

redis_max_connections = 20


class BaseRedisManager(object):
    def __init__(self, host, port, db, password, decode_responses,
                 service_name=None, max_connections=None):
        self._host = host
        self._port = port
        self._db = db
        self._password = password
        self._decode_responses = decode_responses
        self._service_name = service_name
        self._max_connections = max_connections or 10

        self._client_map = {}

    def __del__(self):
        try:
            for conn in self._client_map.values():
                conn.close()
        except:
            pass


class RedisPoolManager(BaseRedisManager):
    def __init__(self, host, port, db, password, decode_responses,
                 service_name=None, max_connections=None, sentinel=None):
        super(RedisPoolManager, self).__init__(
            host, port, db, password, decode_responses,
            service_name=service_name, max_connections=max_connections)

    def get_redis_client(self, db=None):
        db = db or self._db
        if db not in self._client_map:
            self._client_map[db] = self._get_redis_client(db)
        return self._client_map[db]

    def _get_startup_nodes_from_config(self):
        redis_hosts = self._host.split(',')
        redis_ports = self._port if isinstance(self._port, int) else self._port.split(',')
        if len(redis_hosts) != len(redis_ports):
            raise Exception('redis host num is not equal than redis port num')
        startup_nodes = []
        for host, port in zip(redis_hosts, redis_ports):
            startup_nodes.append({'host': host, 'port': port})
        return startup_nodes

    def _get_redis_client(self, db=None):
        db = db or self._db
        startup_nodes = self._get_startup_nodes_from_config()
        if len(startup_nodes) > 1:
            cli = rediscluster.RedisCluster(
                startup_nodes=startup_nodes,
                password=self._password,
                skip_full_coverage_check=True,
                decode_responses=self._decode_responses
            )
        else:
            connection_pool = redis.BlockingConnectionPool(
                host=self._host,
                port=self._port,
                password=self._password,
                db=db, timeout=120,
                max_connections=redis_max_connections,
                decode_responses=self._decode_responses
            )
            cli = redis.StrictRedis(connection_pool=connection_pool)
        return cli


class RedisSentinelManager(BaseRedisManager):

    def __init__(self, host, port, db, password, decode_responses,
                 service_name, sentinel=None, max_connections=None):
        super(RedisSentinelManager, self).__init__(
            host, port, db, password, decode_responses,
            service_name=service_name, max_connections=max_connections)

        self._sentinel = sentinel

    def init_sentinel(self):
        sentinel_startup_nodes = self._get_startup_nodes_from_config()
        self._sentinel = Sentinel(sentinel_startup_nodes)

    def _get_master_client(self, db):
        try:
            # SentinelConnectionPool内部有服务发现机制
            return self._sentinel.master_for(
                service_name=self._service_name,
                redis_class=redis.StrictRedis,
                db=db,
                socket_timeout=120,
                password=self._password,
                max_connections=redis_max_connections,
                decode_responses=self._decode_responses
            )
        except Exception as e:
            raise e

    def _get_startup_nodes_from_config(self):
        redis_hosts = self._host.split(',')
        redis_ports = self._port if isinstance(self._port, int) else self._port.split(',')
        if len(redis_hosts) != len(redis_ports):
            raise Exception('redis host num is not equal than redis port num')
        startup_nodes = []
        for host, port in zip(redis_hosts, redis_ports):
            startup_nodes.append((host, port))
        return startup_nodes

    def get_redis_client(self, db=None):
        db = db or self._db
        if not self._sentinel:
            self.init_sentinel()
        if db not in self._client_map:
            self._client_map[db] = self._get_master_client(db)
        return self._client_map[db]


__all__ = [
    'RedisPoolManager',
    'RedisSentinelManager'
]
