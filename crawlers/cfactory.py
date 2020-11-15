# cfactory.py -- Module for crawler's factory class
#
# This module contains `CrawlerFactory` which is the factory
# class for all crawlers that are supported


import crawlers.wuxiaworld
import crawlers.lightnovelworld

class CrawlerFactory:

    # The value of DEFAULT_WEB can only be changed by setweb command
    DEFAULT_WEB = 'wuxiaworld'
    SUPPORTED_WEBS = {
        'wuxiaworld': ['Wuxiaworld.com', crawlers.wuxiaworld.WuxiaWorldCrawler],
        'lnworld':    ['LightNovelWorld.com', crawlers.lightnovelworld.LightNovelWorldCrawler]
    }

    def get_crawler(self, novel):
        """
        Return a crawler instance of the default website. We are guaranteed that it's a
        valid website that is supported.
        """
        crawler = self.SUPPORTED_WEBS[CrawlerFactory.DEFAULT_WEB][1]
        return crawler(novel)