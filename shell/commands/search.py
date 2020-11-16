# search.py -- Searches for a novel in a particular website

import shell.cmdbase
import shell.format_utils.result_formatter as res_fmt
import crawlers.cfactory as cfactory
import crawlers.cbase as cbase


class SearchCommand(shell.cmdbase.CommandBase):
    """
    search -- Searches for novels on the website that was set using setweb command
    Usage: search <keyword>

    Example: search --novel "gods"
    """
    DESCRIPTION = 'Searches for novels based on a keyword that is entered'
    ERR_NO_KEYWORD_MSG = 'Ummm...please enter a keyword to search ?'

    def __init__(self):
        super().__init__()
        self.description = self.DESCRIPTION

    def help(self):
        return self.__doc__

    def execute(self, cmd_args):
        """
        Search for the keyword and return the results (if any)
        If no result is found, then returns an error message
        """

        # If there was only one argument, i.e. the command itself,
        # then this is an error
        if not cmd_args:
            return self.CMD_STATUS_ERROR, res_fmt.res_format_error(self.ERR_NO_KEYWORD_MSG)

        # Alright, this means there is atleast one keyword to search for
        # Join everything, split by spaces
        keyword = ' '.join(cmd_args)

        crawler = cfactory.CrawlerFactory()
        web_crawler = crawler.get_crawler(keyword)

        # Search for it in the corresponding website and fetch the results
        status, contents = web_crawler.search()

        if status == cbase.CrawlerBase.CRAWLER_STATUS_ERR:
            return self.CMD_STATUS_ERROR, res_fmt.res_format_error(contents)

        # Else it means the search was a success, the contents hold the list of dictionaries
        # Need to parse it and return as a formatted text object
        fmt_search_res = self._parse_result([contents, keyword])
        return self.CMD_STATUS_SUCCESS, fmt_search_res

    def _parse_args(self, cmd_args):
        pass

    def _parse_result(self, results):
        """ Parse the result of the search command and return it """
        contents = results[0]
        keyword  = results[1]
        return res_fmt.res_format_search(contents, keyword)
