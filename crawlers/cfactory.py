# cfactory.py -- Module for crawler's factory class
#
# This module contains `CrawlerFactory` which is the factory
# class for all crawlers that are supported


import crawlers.wuxiaworld

class CrawlerFactory:

    # The value of DEFAULT_WEB can only be changed by setweb command
    DEFAULT_WEB = 'wuxiaworld'
    SUPPORTED_WEBS = {
        'wuxiaworld': crawlers.wuxiaworld.WuxiaWorldCrawler
    }

    def __init__(self) -> None:
        raise NotImplementedError

    def get_crawler(self, novel):
        """
        Return a crawler instance of the default website. We are guaranteed that it's a
        valid website that is supported.
        """
        return self.SUPPORTED_WEBS[self.DEFAULT_WEB](novel)