import pytest
from page_analyzer.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


def test_index_route(client):
    response = client.get('/')
    html = response.data.decode()

    assert response.status_code == 200
    assert '<a class="navbar-brand" href="/">Анализатор страниц</a>' in html
    assert '<p class="lead">Бесплатно проверяйте сайты на SEO пригодность</p>' in html
    assert '<a class="nav-link " href="/urls">Сайты</a>' in html


def test_404(client):
    response = client.get('/qwerty')
    html = response.data.decode()

    assert response.status_code == 404
    assert '<h1>Страница не найдена</h1>' in html


def test_add_url_wrong_data(client):
    response = client.post('/urls', data={"url": "wrong_data"}, follow_redirects=True)
    assert response.status_code == 422


@pytest.fixture
def test_existing_url_redirect(app, mocker):
    mocker.patch('app.get_urls_by_name', return_value={'id': 1})
    response = app.test_client().post('/urls', data={'url': 'https://www.example.com'})
    assert response.status_code == 302  # Redirect
    assert response.location == f'http://localhost/url/1'
    assert 'Страница уже существует' in response.data


@pytest.fixture
def test_missing_url_error(app):
    response = app.test_client().post('/urls', data={})
    assert response.status_code == 422  # Unprocessable Entity
    assert 'URL обязателен' in response.data


@pytest.fixture
def test_invalid_id_error(app):
    response = app.test_client().post('/urls/20000/checks')
    assert response.status_code == 404  # Not Found


@pytest.fixture
def test_url_show(client, mock_get_urls_by_id, mock_get_checks_by_id):
    # Mock the response of get_urls_by_id function
    mock_get_urls_by_id.return_value = {'id': 1, 'name': 'http://example.com'}

    # Mock the response of get_checks_by_id function
    mock_get_checks_by_id.return_value = [
        {'id': 1, 'url_id': 1, 'status_code': 200, 'response_time': 0.5, 'checked_at': '2022-01-01 12:00:00'},
        {'id': 2, 'url_id': 1, 'status_code': 404, 'response_time': 0.3, 'checked_at': '2022-01-02 12:00:00'}
    ]

    # Make a GET request to the URL show endpoint
    response = client.get('/urls/1')

    # Check that the response status code is 200 OK
    assert response.status_code == 200

    # Check that the response contains the URL name
    assert b'<h1>http://example.com</h1>' in response.data

    # Check that the response contains the check data
    assert b'200' in response.data
    assert b'0.5' in response.data
    assert b'2022-01-01 12:00:00' in response.data