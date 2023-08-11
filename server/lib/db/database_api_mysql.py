from lib.utils.db_utils import sql_query
from lib.db.base.mysql_base import get_mysql_db_cursor


def get_question_sentence():
    cursor, conn = get_mysql_db_cursor()
    sql = """
    SELECT
        s_id,
        en_s,
        ch_s,
        en_k
    FROM
        sentence
    WHERE
        delete_flag = 0
    """
    try:
        sql_query(cursor, sql)
        data = list(cursor.fetchall())
    finally:
        cursor.close()
        conn.close()
    return data
