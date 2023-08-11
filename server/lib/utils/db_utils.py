import time

from lib import get_logger

logger = get_logger(__name__)


def sql_query(cursor, sql):
    """

    Args:
        cursor:
        sql:

    Returns:

    """
    start_time = time.time()
    cursor.execute(sql)
    end_time = time.time()
    if end_time - start_time > 10:
        logger.warn('[LONG_TIME_QUERY] sql "{}" takes {}s'.format(sql, end_time - start_time))
