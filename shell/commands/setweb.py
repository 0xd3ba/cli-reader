# setweb.py -- Sets the default website to use

import shell.cmdbase
import shell.format_utils.result_formatter as res_fmt
import crawlers.cfactory as cfactory


class SetWebCommand(shell.cmdbase.CommandBase):
    """
    setweb -- Sets the website to use for searches
    Usage: setweb <website>

    Example: setweb wuxiaworld
    """
    DESCRIPTION = 'Set the website to use for reading/searching'
    ERR_INVALID_WEB_MSG = 'Website entered is not a valid ID. Please check using "listwebs"'
    ERR_NO_WEB_MSG = "Website can't be changed if you don't enter a website ID ?"
    WEB_CHANGE_MSG = "Website has been changed to: "

    def __init__(self):
        super().__init__()
        self.description = self.DESCRIPTION

    def help(self):
        return self.__doc__

    def execute(self, cmd_args):
        """
        Check if the entered website is a valid supported website
        If yes, then change to it; else throw an error
        """
        if not cmd_args:
            return self.CMD_STATUS_ERROR, res_fmt.res_format_error(self.ERR_NO_WEB_MSG)

        # Get the website -- The first item in the list
        web_id = cmd_args[0]
        supp_websites = cfactory.CrawlerFactory.SUPPORTED_WEBS

        if web_id not in supp_websites.keys():
            return self.CMD_STATUS_ERROR, res_fmt.res_format_error(self.ERR_INVALID_WEB_MSG)

        # A valid website, change the static class variable of the crawler factory
        cfactory.CrawlerFactory.DEFAULT_WEB = web_id

        website_name = supp_websites[web_id][0]
        succ_msg = self.WEB_CHANGE_MSG + web_id + f' ({website_name})'

        return self.CMD_STATUS_SUCCESS, self._parse_result(succ_msg)


    def _parse_args(self, cmd_args):
        pass

    def _parse_result(self, result):
        return res_fmt.res_format_setweb(result)
