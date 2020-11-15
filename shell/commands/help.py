# help.py -- Displays information about the command

from prompt_toolkit import print_formatted_text
import crawlers.cbase
import shell.cmdbase
import shell.cmdfactory as cmdfactory


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
        args = cmd_args
        cmdFactoryObj = cmdfactory.CommandFactory()
        result = {}
        if len(args) == 0:
            for key in cmdFactoryObj.SUPPORTED_CMDS.keys():
                result[key] = cmdFactoryObj.get_command(key).DESCRIPTION

        elif len(args) == 1:
            result[args[0]] = cmdFactoryObj.get_command(args[0]).help()
        else:
            for cmd in args:
                result[cmd] = cmdFactoryObj.get_command(cmd).DESCRIPTION
        # there's no case for status_code 0
        return 0, self._parse_result(result)

    def _parse_args(self, cmd_args):
        pass  # No need of argparse for this command

    def _parse_result(self, results):
        # TODO: Parse the result accordingly
        for item in results:
            text = str(item) + ' : ' + str(results[item]) + '\n'
            print_formatted_text(text)

        return results
