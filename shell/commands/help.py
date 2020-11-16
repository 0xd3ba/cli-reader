# help.py -- Displays information about the command

import crawlers.cbase
import shell.cmdbase
import shell.cmdfactory as cmdfactory
import shell.format_utils.result_formatter as res_fmt


class HelpCommand(shell.cmdbase.CommandBase):
    """
    help -- Displays information about a (or multiple) command(s)
    Usage: help [<command_1> <command_2> ... ]
    """

    DESCRIPTION = 'Displays information about a command or multiple commands'

    def __init__(self):
        super().__init__()
        self.description = self.DESCRIPTION

    def help(self):
        return self.__doc__

    def execute(self, cmd_args):
        """ Displays the information about the commands specified in the list """

        cmds_dict = cmdfactory.CommandFactory.SUPPORTED_CMDS
        result_dict = {}

        # This is the case when information about all the commands need to be returned
        if not cmd_args:

            for cmd in cmds_dict.keys():
                cmd_obj = cmds_dict[cmd]
                result_dict[cmd] = cmd_obj.DESCRIPTION

            return self.CMD_STATUS_SUCCESS, res_fmt.res_format_help_mult(result_dict)

        # This is the case when there are multiple commands in the list
        elif len(cmd_args) > 1:
            for cmd in cmd_args:
                cmd_obj = cmds_dict.get(cmd, cmdfactory.CommandFactory.DEF_CMD)
                result_dict[cmd] = cmd_obj.DESCRIPTION

            return self.CMD_STATUS_SUCCESS, res_fmt.res_format_help_mult(result_dict)

        # This means information is needed only about a single command
        # Assume the command is an incorrect command, then update the message accordingly
        cmd = cmd_args[0]
        result_dict[cmd] = cmdfactory.CommandFactory.DEF_CMD.INVALID_COMMAND_MSG
        if cmd in cmds_dict.keys():
            result_dict[cmd_args[0]] = cmds_dict[cmd]().help()

        # By now the result_dict was populated appropriately, parse it and return it to the caller
        return self.CMD_STATUS_SUCCESS, self._parse_result(result_dict)


    def _parse_args(self, cmd_args):
        pass  # No need of argparse for this command

    def _parse_result(self, result):
        # This method is only called when there is a single result to parse
        # Bad way to do things but it gets the job done though
        return res_fmt.res_format_help_single(result)
