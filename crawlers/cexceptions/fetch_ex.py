# fetch_ex.py -- Exception class for errors due to fetching a page

import crawlers.cexceptions.exbase as crex


class FetchHttpError(crex.CrawlerExceptionBase):
    """
    FetchHttpError -- Exception for when HTTP errors occur during fetching
    """

    HTTP_ERR_MSG = "HTTP Error with following status code: "
    HTTP_ERR_URL = "URL: "

    def __init__(self, url, httpresp):
        super().__init__()
        self.status = httpresp.status_code
        self.url = url

    def handler(self):
        self.fmt_msg = self.prepare_msg()
        return self.fmt_msg

    def prepare_msg(self):
        fmt_msg = self.HTTP_ERR_MSG + str(self.status)
        fmt_msg += '\n' + self.HTTP_ERR_URL + self.url
        return fmt_msg


class FetchConnectionError(crex.CrawlerExceptionBase):
    """
    FetchConnectionError -- Exception for when connection error
    """

    CONN_ERR_MSG = "Connection to the website failed. Please check your internet connectivity"

    def __init__(self):
        super().__init__()

    def handler(self):
        self.fmt_msg = self.prepare_msg()
        return self.fmt_msg

    def prepare_msg(self):
        return self.CONN_ERR_MSG


class FetchURLError(crex.CrawlerExceptionBase):
    """
    FetchURLError -- Exception for URL errors occur due to invalid URLs
    """

    URL_ERR_MSG = "The following URL is invalid: "

    def __init__(self, url):
        super().__init__()
        self.url = url

    def handler(self):
        self.fmt_msg = self.prepare_msg()
        return self.fmt_msg

    def prepare_msg(self):
        return self.URL_ERR_MSG


class FetchTimeoutError(crex.CrawlerExceptionBase):
    """
    FetchTimeoutError -- Exception for Connection timeout errors
    """

    TIMEOUT_ERR_MSG = "Connection Timed out to the following URL: "

    def __init__(self, url):
        super().__init__()
        self.url = url

    def handler(self):
        self.fmt_msg = self.prepare_msg()
        return self.fmt_msg

    def prepare_msg(self):
        return self.TIMEOUT_ERR_MSG + self.url

