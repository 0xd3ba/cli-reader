# addfav.py -- Command that adds currently reading novel to favorites

import shell.cmdbase


class AddFavoritesCommand(shell.cmdbase.CommandBase):
    """
    addfav -- Add a novel to favorites
    TODO: Add information about the command
    """
    DESCRIPTION = 'Adds a chapter of a novel to a favourite list'

    def __init__(self):
        super().__init__()
        # TODO: Add specific instance variables

    def help(self):
        pass

    def execute(self, cmd_args):
        pass

    def _parse_args(self, cmd_args):
        pass

    def _parse_result(self, result):
        pass
