import psycopg2
from psycopg2.extras import DictCursor

from tokens import Tokens


def _fetch_one_wrapper(method):
    """Monkey patch of method cursor.fetchone()
    Converts row rows from psycopg2.extras.DictRow to dicts
    """
    def wrapper(*args, **kwargs):
        if (row := method(*args, **kwargs)) is not None:
            return dict(row)
        else:
            return row

    return wrapper


def _fetch_all_wrapper(method):
    """Monkey patch of method cursor.fetchall()
    Converts all rows from psycopg2.extras.DictRow to dicts
    """
    def wrapper(*args, **kwargs):
        rows = method(*args, **kwargs)
        return [dict(row) for row in rows]

    return wrapper


def get_psql_cursor() -> DictCursor:
    """Returns postgresql cursor"""
    connection = psycopg2.connect(
        user=Tokens.PSQL_USER,
        password=Tokens.PSQL_PASSWORD,
        host=Tokens.PSQL_HOST,
        port=Tokens.PSQL_PORT,
        database=Tokens.PSQL_DATABASE
    )
    connection.autocommit = True
    cursor = connection.cursor(cursor_factory=DictCursor)
    cursor.fetchone = _fetch_one_wrapper(cursor.fetchone)
    cursor.fetchall = _fetch_all_wrapper(cursor.fetchall)
    return cursor
