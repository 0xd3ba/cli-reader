# cmdbase.py -- The base class for all the shell commands

import argparse
import sys


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        raise Exception()


class CommandBase:
    """
    CommandBase -- Base class for all the supported shell commands
    """

    def __init__(self):
        # The argument parser for the command
        self.arg_parser = ArgumentParser()
        self.description = None

    def help(self):
        """
        Returns the following information about the command:
            - Command Name
            - Command Flags
            - Usage
            - Example
        Else list the supported commands
        """
        raise NotImplementedError

    def execute(self, cmd_args: str):
        """
        Executes the command with the given keyword arguments
        """
        raise NotImplementedError

    def _parse_args(self, cmd_args: str):
        """
        Responsible for parsing the command line arguments of the command
        and returning a dictionary object
        :return:
        """
        raise NotImplementedError

    def _parse_result(self, result):
        """
        Responsible for parsing the result of the command and returning it
        """
        raise NotImplementedError
