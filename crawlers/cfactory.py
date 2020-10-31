# cfactory.py -- Module for crawler's factory class
#
# This module contains `CrawlerFactory` which is the factory
# class for all crawlers that are supported

class CrawlerFactory:
    def __init__(self) -> None:
        raise NotImplementedError

    def get_crawler(self, website):
        raise NotImplementedError