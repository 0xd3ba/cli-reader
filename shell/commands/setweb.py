# setweb.py -- Sets the default website to use

import shell.cmdbase
import crawlers.cfactory as cfactory
import shlex


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
        # TODO: Add specific instance variables

    def help(self):
        return self.__doc__

    def execute(self, cmd_args):
        args = self._parse_args(cmd_args)
        crawler = cfactory.CrawlerFactory()
        all_websites = crawler.SUPPORTED_WEBS.keys()
        if args.website in all_websites:
            crawler.DEFAULT_WEB = args.website
        # else:
        #     # Throw Error

    def _parse_args(self, cmd_args):
        self.arg_parser.add_argument(
            '-w', '--website', type=str, required=True, help='Name of the website')
        args = self.arg_parser.parse_args(shlex.split(cmd_args))
        return args

    def _parse_result(self, result):
        return result
