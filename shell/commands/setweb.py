# setweb.py -- Sets the default website to use

import shell.cmdbase

class SetWebCommand(shell.cmdbase.CommandBase):
    """
    setweb -- Sets the website to use for searches
    Usage: setweb [ -w | --website ] <website>

    Example: setweb -w wuxiaworld
    """

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