# defcmd.py -- Default command that is executed when user enters an invalid command

import shell.cmdbase
import shell.format_utils.result_formatter as res_fmt


class DefaultCommand(shell.cmdbase.CommandBase):
    """
    DefaultCommand is executed when user inputs some illegal command
    """
    INVALID_COMMAND_MSG = "Invalid Command. Please enter a valid Command. Use Help!"

    # This is done to ensure symmetry between the various commands. Description about this
    # command is only accessed from `help` command when the user enters an invalid command
    # in the argument list to help -- So it doesn't affect any other thing, hence this is
    # something that's kind of acceptable
    DESCRIPTION = INVALID_COMMAND_MSG

    def __init__(self):
        super().__init__()
        # TODO: Add specific instance variables

    def help(self):
        pass

    def execute(self, cmd_args):
        return self.CMD_STATUS_ERROR, self._parse_result(self.INVALID_COMMAND_MSG)

    def _parse_args(self, cmd_args):
        pass

    def _parse_result(self, result):
        return res_fmt.res_format_error(result)
