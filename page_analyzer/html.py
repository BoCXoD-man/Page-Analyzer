import requests
from bs4 import BeautifulSoup


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
