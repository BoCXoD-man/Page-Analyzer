from psycopg2.extras import RealDictCursor
import validators
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from psycopg2 import connect
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def get_connect_db():
    """
    CLI is a utility.
    :return: the connection to the database.
    """

    conn = connect(DATABASE_URL)
    return conn


def validate_url(url):
    """
    Validation and normalization for the entered URL. The URL must have a valid
    address, it is mandatory and does not exceed 255 characters.
    :param url: Site URL.
    :return: Dict of normalized url and errors if any.
    """

    error = None

    if len(url) == 0:
        error = 'zero'
    elif len(url) > 255:
        error = 'length'
    elif not validators.url(url):
        error = 'invalid'
    else:
        parsed_url = urlparse(url)
        norm_url = f'{parsed_url.scheme}://{parsed_url.netloc}'

        found = get_urls_by_name(norm_url)

        if found:
            error = 'exists'

        url = norm_url

    valid = {'url': url, 'error': error}

    return valid


def get_url_data(url: str) -> dict:
    """
    Request provided URL. Save response code. Parse the page and check the
    presence of <h1>, <title> and <meta name="description" content="...">
    tags on the page.
    :param url: Site URL.
    :return: Dict of parsed and found data.
    """

    r = requests.get(url)

    if r.status_code != 200:
        raise requests.RequestException

    check = {'status_code': r.status_code}

    soup = BeautifulSoup(r.text, 'html.parser')

    h1_tag = soup.find('h1')
    title_tag = soup.find('title')
    description_tag = soup.find('meta', attrs={'name': 'description'})

    check['h1'] = h1_tag.text.strip() if h1_tag else ''
    check['title'] = title_tag.text.strip() if title_tag else ''
    check['description'] = description_tag['content'].strip() \
        if description_tag else ''

    return check


def add_check(check: dict) -> None:
    """
    Insert into database new check data.
    Tables: url_checks
    :param check: Dict containing url check data: URL id, check status code, h1,
    title, description, check date
    """

    conn = get_connect_db()
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
        conn.commit()
    conn.close()


def get_checks_by_id(id_url: int) -> dict:
    """
    Query the database for all URL checks.
    Tables: url_checks
    :param id_url: URL id.
    :return: Dict containing checks info: id, status code, h1, title,
    description, check date.
    """

    conn = get_connect_db()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        q_select = '''SELECT *
        FROM url_checks
        WHERE url_id=(%s)
        ORDER BY id DESC'''
        cur.execute(q_select, [id_url])
        checks = cur.fetchall()
    conn.close()

    return checks


def get_urls_by_name(name: str) -> dict:
    """
    Query the database for one URL data based on its name.
    Tables: urls
    :param name: URL name.
    :return: Dict containing one url data: id, name, creation date.
    """

    conn = get_connect_db()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        q_select = '''SELECT *
        FROM urls WHERE name=(%s)'''
        cur.execute(q_select, [name])
        urls = cur.fetchone()
    conn.close()

    return urls
