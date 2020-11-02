# defcmd.py -- Default command that is executed when user enters an invalid command

import shell.cmdbase


class DefaultCommand(shell.cmdbase.CommandBase):
    """
    TODO: Add information about the command
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
