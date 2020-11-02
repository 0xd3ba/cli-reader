# search.py -- Searches for a novel in a particular website

import shell.cmdbase
import crawlers.cfactory as cfactory
import shlex

class SearchCommand(shell.cmdbase.CommandBase):
    """
    search -- Searches for novels on the website that was set using setweb command
    Usage: search [ -n | --novel ] <keyword>

    Example: search --novel "gods"
    """
    DESCRIPTION = 'Searches for novels based on a keyword that is entered'

    def __init__(self):
        super().__init__()
        self.description = self.DESCRIPTION

    def help(self):
        return self.__doc__

    def execute(self, cmd_args):
        args = self._parse_args(cmd_args)
        crawler = cfactory.CrawlerFactory()
        web_crawler = crawler.get_crawler(args.novel)
        results = web_crawler.search()
        if results == None:
            return -1,None
        return 0,self._parse_result(results)

    def _parse_args(self, cmd_args):
        self.arg_parser.add_argument('-n', '--novel', type= str,required=True, help= 'Name of the Novel')
        args = self.arg_parser.parse_args(shlex.split(cmd_args))
        return args

    def _parse_result(self, result):
        # TODO: Parse the result accordingly
        return result
