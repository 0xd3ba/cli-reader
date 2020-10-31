# fetcher.py -- Request a webpage from the website

import requests
from requests.exceptions import HTTPError
from requests.exceptions import InvalidURL

# This consists of the HTTP headers to include in the request message
HTTP_REQ_HEADERS = {
    'user-agent': 'Mozilla'
    # Add custom HTTP request headers if required
}


def fetch(url):
    """
    Fetch the file from the `url` and return the contents
    Write the status of the request to the log as well
    """
    response = None
    try:
        response = requests.get(url, headers=HTTP_REQ_HEADERS)
    except HTTPError as herr:
        pass
    except InvalidURL as ierr:
        pass

    return response