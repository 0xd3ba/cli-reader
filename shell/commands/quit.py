# quit.py -- Exit the shell

import shell.cmdbase


class QuitCommand(shell.cmdbase.CommandBase):
    """
    quit -- Exit the shell gracefully
    Usage: quit
    """
    DESCRIPTION = 'Quits the Application'

    def __init__(self):
        super().__init__()

    def help(self):
        return self.__doc__

    def execute(self, cmd_args):
        """ Simply does an exit(0) (~_~) """
        exit(0)

    def _parse_args(self, cmd_args):
        # Parsing of arguments is not needed here
        pass

    def _parse_result(self, result):
        # Parsing of results is not needed here
        pass
