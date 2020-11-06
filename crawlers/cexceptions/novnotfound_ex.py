# novnotfound_ex.py -- Exception class when a novel is not found in searches

import crawlers.cexceptions.exbase as crex


class NovelNotFoundError(crex.CrawlerExceptionBase):
    NNOTFOUND_MSG = "No search results with the following keyword: "

    def __init__(self, keyword):
        super().__init__()
        self.keyword = keyword  # The keyword that was used for search

    def handler(self):
        self.fmt_msg = self.prepare_msg()
        return self.fmt_msg

    def prepare_msg(self):
        # For the time being simply return an identity mapping of the message
        return self.NNOTFOUND_MSG + self.keyword
