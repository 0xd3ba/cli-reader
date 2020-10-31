# cmdbase.py -- The base class for all the shell commands

import argparse

class CommandBase:
    """
    CommandBase -- Base class for all the supported shell commands
    """

    def __init__(self):
        self.arg_parser = argparse.ArgumentParser()  # The argument parser for the command

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

    def execute(self, **kwargs):
        """
        Executes the command with the given keyword arguments
        """
        raise NotImplementedError

    def _parse_args(self, cmd_args:str):
        """
        Responsible for parsing the command line arguments of the command
        and returning a dictionary object
        :return:
        """
        raise NotImplementedError

    def _parse_result(self, **kwargs):
        """
        Responsible for parsing the result of the command and returning it
        """
        raise NotImplementedError