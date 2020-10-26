# cbase.py -- The base class for all crawlers
#
# This module contains the base class `CrawlerBase`
# that all website crawlers must implement. This is
# the API that's made available to the interactive shell


class CrawlerBase:
    def __init__(self):
        pass

    def get_chapter(self, chap_num: int) -> dict:
        """
        Given a chapter number of some novel, return a dictionary object
        of the chapter contents (see cutils package).
        If no such chapter exists, raises a ChapterNotFoundError exception
        """
        raise NotImplementedError

    def next_chapter(self) -> dict:
        """
        Returns the next chapter relative to the current chapter.
        If no such chapter exists, raises a ChapterNotFoundError exception
        """
        raise NotImplementedError

    def previous_chapter(self) -> dict:
        """
        Returns the previous chapter relative to the current chapter.
        If no such chapter exists, raises a ChapterNotFoundError exception
        """
        raise NotImplementedError

    def search(self, keyword: str) -> dict:
        """
        Searches for `keyword` in the corresponding website and returns a dictionary
        object of the results
        """
        raise NotImplementedError

    def get_summary(self, novel_name) -> dict:
        """
        Gets the summary of the novel titled `novel_name` as a dictionary object
        """
        raise NotImplementedError