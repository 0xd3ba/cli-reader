# search.py -- Searches for a novel in a particular website
from __future__ import unicode_literals, print_function
import shell.cmdbase
import crawlers.cfactory as cfactory
import shlex
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style


class SearchResultModel():
    def __init__(self):
        self.style = Style.from_dict({
            'heading': '#ff0066',
            'name': '#ff0066',
            'tags': '#44ff00 italic',
            'synopsis': '#ffffff',
        })
        self.res_keys = ['name', 'tags', 'synopsis', 'author']

    def format_result(self, singleResult, i):
        for key in self.res_keys:
            if key not in singleResult:
                singleResult[key] = None
        name = 'Name : ' + singleResult['name'] + '\n'+'-' * \
            50 + '\n' if singleResult['name'] != None else ''
        author = 'Author : ' + singleResult['author'] + '\n'+'-' * \
            50 + '\n' if singleResult['author'] != None else ''
        tags = 'Tags : [ ' + ', '.join(singleResult['tags']) + \
            ' ]' + '\n'+'-'*50+'\n' if singleResult['tags'] != None else ''
        synopsis = 'Synopsis : [ ' + '\n'.join(singleResult['synopsis']) + ' ]' \
            if singleResult['synopsis'] != None else ''

        formatted_result = FormattedText([
            ('class:heading', 'Result No : ' + str(i) + '\n'+'-'*50 + '\n'),
            ('class:name', name),
            ('class:name', author),
            ('class:tags', tags),
            ('class:synopsis', synopsis),
            ('', '\n\n'),
        ], auto_convert=True)
        return formatted_result


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
        self.arg_parser.add_argument(
            'novelname', nargs='+', type=str, help='Name of the Novel')

    def help(self):
        return self.__doc__

    def execute(self, cmd_args):
        args = self._parse_args(cmd_args)
        crawler = cfactory.CrawlerFactory()
        novel = ' '.join(args.novelname)
        web_crawler = crawler.get_crawler(novel)
        results = web_crawler.search()
        if results[0] == -1:
            return results
        return 0, self._parse_result(results[1])

    def _parse_args(self, cmd_args):
        args = self.arg_parser.parse_args(cmd_args)
        return args

    def _parse_result(self, results):
        result_model = SearchResultModel()
        i = 0
        for item in results:
            formatted_res = result_model.format_result(item, i)
            print_formatted_text(formatted_res, style=result_model.style)
            i = i + 1
        return results
