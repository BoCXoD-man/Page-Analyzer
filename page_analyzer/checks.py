
import validators
from urllib.parse import urlparse

from page_analyzer.db import get_urls_by_name


def validate_url(url):
    """
    Validation and normalization for the entered URL. The URL have a valid
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
