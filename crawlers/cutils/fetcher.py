# fetcher.py -- Request a webpage from the website

import requests

from crawlers.cexceptions.fetch_ex import FetchHttpError
from crawlers.cexceptions.fetch_ex import FetchURLError
from crawlers.cexceptions.fetch_ex import FetchConnectionError
from crawlers.cexceptions.fetch_ex import FetchTimeoutError


# The timeout interval beyond which Timeout exception occurs
CONN_TIMEOUT = 10

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
    try:
        response = requests.get(url, headers=HTTP_REQ_HEADERS, timeout=CONN_TIMEOUT)
        response.raise_for_status()          # Check if valid HTTP response - HTTPError is raised otherwise
        return response

    # If there is no internet connectivity
    except requests.ConnectionError as cerr:
        raise FetchConnectionError()

    # If the response's status code is not 200 (OK)
    except requests.HTTPError:
        raise FetchHttpError(url)

    # If there was a timeout during the request
    except requests.Timeout:
        raise FetchTimeoutError(url)

    # This can only occur due to invalid URL
    except requests.RequestException:
        raise FetchURLError(url)