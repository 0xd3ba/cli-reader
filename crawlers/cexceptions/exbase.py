# exbase.py -- Base class for all the crawler related exceptions


class CrawlerExceptionBase(Exception):
    """
    CrawlerExceptionBase -- The base class for the exceptions related to crawlers
    """
    def __init__(self):
        self.fmt_msg = None     # The formatted message of the error cause

    def handler(self):
        """
        Do the appropriate tasks required to handle this exception
        """
        raise NotImplementedError

    def prepare_msg(self):
        """
        Prepare the formatted message to return to the shell
        """
        raise NotImplementedError