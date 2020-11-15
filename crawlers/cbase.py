# cbase.py -- The base class for all crawlers
#
# This module contains the base class `CrawlerBase`
# that all website crawlers must implement. This is
# the API that's made available to the interactive shell


class CrawlerBase:

    DEFAULT_HTML_PARSER = 'lxml'
    SEARCH_EMPTY_MSG = "No search results found with the following keyword: "
    NO_NEXT_CHAP_MSG = "There is no next chapter (yet), the current one is the latest one"
    NO_PREV_CHAP_MSG = "There is no previous chapter prior to this chapter"

    # Few status codes that are same in all crawlers
    CRAWLER_STATUS_OK    = 0     # Everything worked fine
    CRAWLER_STATUS_ERR   = -1    # Some error has occured during crawling
    CRAWLER_GET_MULT_RES = -2    # For the case when more than one novel was found in the search inside get_chapter


    def get_chapter(self, chap_num: int) -> (int, any):
        """
        Given a chapter number of some novel, return a dictionary object
        of the chapter contents (see cutils package).
        """
        raise NotImplementedError

    def next_chapter(self) -> (int, any, any):
        """
        Returns the next chapter relative to the current chapter.
        """
        raise NotImplementedError

    def previous_chapter(self) -> (int, any, any):
        """
        Returns the previous chapter relative to the current chapter.
        """
        raise NotImplementedError

    def search(self) -> (int, any):
        """
        Searches for the novel (saved as instance variable) in the corresponding
        website and returns a dictionary object of the results
        """
        raise NotImplementedError