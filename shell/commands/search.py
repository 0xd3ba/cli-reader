# search.py -- Searches for a novel in a particular website

import shell.cmdbase

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
        pass

    def execute(self, cmd_args):
        pass

    def _parse_args(self, cmd_args):
        pass

    def _parse_result(self, result):
        # TODO: Parse the result accordingly
        return result