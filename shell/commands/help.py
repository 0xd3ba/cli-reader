# help.py -- Displays information about the command

import argparse

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
        args = self._parse_args(cmd_args)
        cmdFactoryObj = cmdfactory.CommandFactory()
        result = {}
        if len(args) == 0 :
        	for key in cmdFactoryObj.SUPPORTED_CMDS.keys():
        		result[key] = cmdFactoryObj.get_command(key).DESCRIPTION
        	
        elif len(args) == 1:
        	result[args[0]] = cmdFactoryObj.get_command(args[0]).help()
        else:
        	for cmd in args:
        		result[cmd] = cmdFactoryObj.get_command(cmd).DESCRIPTION
        return 1,self._parse_result(result)	#there's no case for status_code 0

    def _parse_args(self, cmd_args):
        return cmd_args.split(' ')   # No need of argparse for this command

    def _parse_result(self, result):
    	# TODO: Parse the result accordingly
        return result
