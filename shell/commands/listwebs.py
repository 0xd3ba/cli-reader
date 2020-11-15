# listwebs.py -- Displays all the supported websites

import shell.cmdbase
import shell.format_utils.result_formatter as res_fmt
import crawlers.cfactory as cfactory

from prompt_toolkit import print_formatted_text


class ListWebsCommand(shell.cmdbase.CommandBase):
    """
    listwebs -- Lists the available websites supported
    """
    DESCRIPTION = 'List all the websites that are currently supported'
    LIST_HEADER = ['ID', 'Website Name']

    def __init__(self):
        super().__init__()
        self.description = self.DESCRIPTION

    def help(self):
        return self.__doc__

    def execute(self, cmd_args):
        """
        Need to return the results as WebsiteKey: WebsiteName
        """

        # Dictionary of the form:
        #    'website_key': [Website_Name, Website_Crawler_Reference]
        supported_webs = cfactory.CrawlerFactory.SUPPORTED_WEBS
        webkeys  = supported_webs.keys()
        webnames = [item[0] for item in supported_webs.values()]

        parsed_result = self._parse_result([webkeys, webnames])
        return self.CMD_STATUS_SUCCESS, parsed_result

    def _parse_args(self, cmd_args):
        pass

    def _parse_result(self, result):
        """Formats the result and returns it"""
        webkeys  = result[0]
        websites = result[1]

        fmt_result = res_fmt.res_format_listwebs(webkeys,
                                                 websites,
                                                 header_idcol=self.LIST_HEADER[0],
                                                 header_webcol=self.LIST_HEADER[1])
        return fmt_result
