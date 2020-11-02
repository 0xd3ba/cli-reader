# help.py -- Displays information about the command

import argparse

import crawlers.cbase
import shell.cmdbase

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
        pass

    def _parse_args(self, cmd_args):
        return cmd_args.split(' ')   # No need of argparse for this command

    def _parse_result(self, result):
        pass