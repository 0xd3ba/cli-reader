# setweb.py -- Sets the default website to use

import shell.cmdbase
import crawlers.cfactory as cfactory
import shlex
from prompt_toolkit import print_formatted_text


class SetWebCommand(shell.cmdbase.CommandBase):
    """
    setweb -- Sets the website to use for searches
    Usage: setweb [ -w | --website ] <website>

    Example: setweb -w wuxiaworld
    """
    DESCRIPTION = 'Set the website to use for searches'

    def __init__(self):
        super().__init__()
        self.description = self.DESCRIPTION
        self.arg_parser.add_argument(
            '-w', '--website', type=str, required=True,
            help='Name of the website.Use listwebs command to know supported ones.')

    def help(self):
        return self.__doc__

    def execute(self, cmd_args):
        args = self._parse_args(cmd_args)
        if args == None:
            return (-1, "error")
        crawler = cfactory.CrawlerFactory()
        all_websites = crawler.SUPPORTED_WEBS.keys()
        if args.website in all_websites:
            crawler.DEFAULT_WEB = args.website
            result = "Default Website has been changed to : " + crawler.DEFAULT_WEB
            return 0, _parse_result(result)
        else:
            result = "Opps!! Default can't ba changed : Website Not Supported."
            return -1, _parse_result(result)

    def _parse_args(self, cmd_args):
        try:
            args = self.arg_parser.parse_args(cmd_args)
        except:
            return None
        return args

    def _parse_result(self, result):
        print_formatted_text(result)
        return result
