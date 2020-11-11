# listwebs.py -- Displays all the supported websites

import shell.cmdbase
import crawlers.cfactory as cfactory
from prompt_toolkit import print_formatted_text


class ListWebsCommand(shell.cmdbase.CommandBase):
    """
    listwebs -- Lists the available websites supported
    """
    DESCRIPTION = 'List all the websites that are available in the CILREADER'

    def __init__(self):
        super().__init__()
        self.description = self.DESCRIPTION
        # TODO: Add specific instance variables

    def help(self):
        return self.__doc__

    def execute(self, cmd_args):
        crawler = cfactory.CrawlerFactory()
        results = list(crawler.SUPPORTED_WEBS.keys())
        return 0, self._parse_result(results)

    def _parse_args(self, cmd_args):
        pass

    def _parse_result(self, result):
        print_formatted_text(result)
        return result
