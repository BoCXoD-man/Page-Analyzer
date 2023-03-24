from psycopg2.extras import RealDictCursor
from psycopg2 import connect
from dotenv import load_dotenv
import os


load_dotenv()


# Connect function:
def get_connection():
    """
    CLI is a utility.
    :return: the connection to the database.
    """

    return connect(os.getenv('DATABASE_URL'))


def close(conn):
    """
    CLI is a utility.
    :do it: close the connection to the database.
    """
    conn.close()


def commit_db(conn):
    """
    CLI is a utility.
    :do it: commit the connection to the database.
    """
    conn.commit()


# Other function:
def add_check(check: dict, conn) -> None:
    """
    Insert into database new check data.
    Tables: url_checks
    :param check: Dict containing url check data: URL id, check status code, h1,
    title, description, check date
    """

    with conn.cursor() as cur:
        q_insert = '''INSERT
        INTO url_checks(
            url_id,
            status_code,
            h1,
            title,
            description,
            created_at)
        VALUES (%s, %s, %s, %s, %s, %s)'''
        cur.execute(q_insert, (
            check['url_id'],
            check['status_code'],
            check['h1'],
            check['title'],
            check['description'],
            check['checked_at']
        ))
        commit_db(conn)


def get_checks_by_id(url_id_: int, conn) -> dict:
    """
    Query the database for all URL checks.
    Tables: url_checks
    :param url_id_: URL id.
    :return: Dict containing checks info: id, status code, h1, title,
    description, check date.
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        q_select = '''SELECT *
        FROM url_checks
        WHERE url_id=(%s)
        ORDER BY id DESC'''
        cur.execute(q_select, [url_id_])
        checks = cur.fetchall()

    return checks


def get_urls_by_name(name: str, conn) -> dict:
    """
    Query the database for one URL data based on its name.
    Tables: urls
    :param name: URL name.
    :return: Dict containing one url data: id, name, creation date.
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        q_select = '''SELECT *
        FROM urls WHERE name=(%s)'''
        cur.execute(q_select, [name])
        urls = cur.fetchone()

    return urls


def add_site(site: dict, conn) -> None:
    """
    Insert into database new URL.
    Tables: urls
    :param site: Dict containing URL and its creation date.
    """

    with conn.cursor() as cur:
        q_insert = '''INSERT
        INTO urls (name, created_at)
        VALUES (%s, %s)'''
        cur.execute(q_insert, (
            site['url'],
            site['created_at']
        ))
        commit_db(conn)


def get_all_urls(conn) -> dict:
    """
    Query the database for all added URLs. Return only the last check info.
    Tables: urls, url_checks
    :return: Dict of all urls, its id's, last check dates and status codes.
    """

    conn.autocommit = True
    curs = conn.cursor(cursor_factory=RealDictCursor)
    curs.execute("""
    SELECT DISTINCT ON (id) *
    FROM urls
    LEFT JOIN (
    SELECT
        url_id,
        status_code,
        created_at AS last_check
    FROM url_checks
    ORDER BY id DESC
    ) AS checks ON urls.id = checks.url_id
    ORDER BY id DESC
    """)
    data_urls = curs.fetchall()
    return data_urls


def get_urls_by_id(url_id_: int, conn) -> dict:
    """
    Query the database for one URL data based on its id.
    Tables: urls
    :param url_id_: URL id.
    :return: Dict containing one url data: id, name, creation date.
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        q_select = '''SELECT *
        FROM urls WHERE id=(%s)'''
        cur.execute(q_select, [url_id_])
        urls = cur.fetchone()

    return urls
