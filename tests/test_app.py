import pytest
from page_analyzer.app import app



@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


def test_index_route(client):
    response = client.get('/')

    assert response.status_code == 200