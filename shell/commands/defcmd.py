# defcmd.py -- Default command that is executed when user enters an invalid command

import shell.cmdbase
from prompt_toolkit import print_formatted_text


class DefaultCommand(shell.cmdbase.CommandBase):
    """
    DefaultCommand is executed when user inputs some illegal command
    """
    INVALID_COMMAND_MSG = "Invalid Commands or Arguments. Please enter valid Command. Use Help!"
    INVALID_COMMAND_STATUS = -1

    def __init__(self):
        super().__init__()
        # TODO: Add specific instance variables

    def help(self):
        pass

    def execute(self, cmd_args):
        return self.INVALID_COMMAND_STATUS, self._parse_result(self.INVALID_COMMAND_MSG)

    def _parse_args(self, cmd_args):
        pass

    def _parse_result(self, result):
        print_formatted_text(result)
