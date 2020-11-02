# quit.py -- Exit the shell

import shell.cmdbase

class QuitCommand(shell.cmdbase.CommandBase):
    """
    quit -- Exit the shell gracefully
    Usage: quit
    """

    def __init__(self):
        super().__init__()

    def help(self):
        return self.__doc__

    def execute(self, cmd_args):
        #TODO: Close any open files, flush to disk..etc
        exit(0)

    def _parse_args(self, cmd_args):
        # Parsing of arguments is not needed here
        pass

    def _parse_result(self, result):
        # Parsing of results is not needed here
        pass