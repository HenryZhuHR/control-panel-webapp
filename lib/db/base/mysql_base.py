from lib import get_mysql_db_info, get_logger
from lib.utils.drivers.mysql_client import ForkSafeMysqlPool


logger = get_logger(__name__)


def get_mysql_db_cursor():
    conn, cursor = mysql_db_conn_pool.get_cursor()
    return cursor, conn


def get_mysql_db_dict_cursor():
    conn, cursor = mysql_db_conn_pool.get_dict_cursor()
    return cursor, conn


host, port, datayes_db, user, password = get_mysql_db_info()

mysql_db_conn_pool = ForkSafeMysqlPool(
    host,
    port,
    user,
    password,
    datayes_db,
    charset='utf8',
    mincached=1,
    maxcached=3,
    maxconnections=5,
    blocking=True,
    read_timeout=3600,
    connect_timeout=3600,
    logger=logger
)
