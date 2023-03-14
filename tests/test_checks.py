import pytest
from requests import RequestException
from page_analyzer.checks import validate_url, get_url_data

from page_analyzer.db import get_all_urls, get_urls_by_id
import os
from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extras import RealDictCursor


@pytest.fixture()
def site():
    urls = {}
    urls['zero'] = {'url': '', 'error': 'zero'}
    urls['invalid'] = {'url': 'url.com', 'error': 'invalid'}
    urls['long'] = {'url': 'https://www.google.com/1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890', 'error': 'length'}
    urls['valid'] = {'url': 'https://devguide.python.org/documentation/style-guide/#style-guide', 'error': ''}

    return urls


@pytest.fixture()
def check():
    checks = {}
    checks['right'] = 'https://www.python.org/'
    checks['wrong'] = 'http://wrong.com'

    return checks


def test_validation_errors(site):
    assert validate_url(site['zero']['url']) == {'url': site['zero']['url'], 'error': 'zero'}
    assert validate_url(site['invalid']['url']) == {'url': site['invalid']['url'], 'error': 'invalid'}
    assert validate_url(site['long']['url']) == {'url': site['long']['url'], 'error': 'length'}

    # valid = 'https://devguide.python.org'
    # assert validate_url(site['valid']['url']) == {'url': valid, 'error': ''}


def test_check(check):
    right = get_url_data(check['right'])
    assert right == {'description': 'The official home of the Python Programming Language', 'h1': '', 'status_code': 200, 'title': 'Welcome to Python.org'}

    with pytest.raises(RequestException):
        get_url_data(check['wrong'])




@pytest.fixture
def test_get_urls_by_id(mocker):
    expected_url_data = {
        'id': 1,
        'name': 'example.com',
        'created_at': '2022-03-12 10:30:00'
    }
    id_ = 1
    expected_query = f"SELECT * FROM urls WHERE id=({id_})"
    mocker.patch.object(connect, 'cursor')
    mock_cursor = connect.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = expected_url_data

    result = get_urls_by_id(id_)

    connect.assert_called_once_with(DATABASE_URL)
    mock_cursor.execute.assert_called_once_with(expected_query, [id_])
    assert result == expected_url_data



@pytest.fixture
def test_get_all_urls(mocker):
    expected_all_urls_data = [
        {
            'id': 3,
            'name': 'google.com',
            'last_check': '2022-03-11 10:30:00',
            'status_code': 200
        },
        {
            'id': 2,
            'name': 'yahoo.com',
            'last_check': '2022-03-10 10:30:00',
            'status_code': 404
        },
        {
            'id': 1,
            'name': 'example.com',
            'last_check': '2022-03-09 10:30:00',
            'status_code': 200
        }
    ]
    mocker.patch.object(connect, 'cursor')
    mock_cursor = connect.return_value.cursor.return_value
    mock_cursor.fetchall.return_value = expected_all_urls_data

    result = get_all_urls()

    connect.assert_called_once_with(DATABASE_URL)
    assert result == expected_all_urls_data