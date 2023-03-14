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
