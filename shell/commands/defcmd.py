# defcmd.py -- Default command that is executed when user enters an invalid command

import shell.cmdbase


class DefaultCommand(shell.cmdbase.CommandBase):
    """
    DefaultCommand is executed when user inputs some illegal command
    """

    def __init__(self):
        super().__init__()
        # TODO: Add specific instance variables

    def help(self):
        pass

    def execute(self, cmd_args):
        result = "Invalid Commands or Arguments. Please enter valid Command. Use Help!"
        return -1, self._parse_result(result) #-1 status code as entered command was illegal

    def _parse_args(self, cmd_args):
        pass

    def _parse_result(self, result):
        # TODO: Parse the result accordingly
        return result
