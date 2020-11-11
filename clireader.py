# clireader.py -- The entry point of the application

import sys
import shell.cmdfactory as cmdfactory
if __name__ == '__main__':

    # Add new path variables
    sys.path.append('crawlers/')
    sys.path.append('shell/')

    cmdFactoryObj = cmdfactory.CommandFactory()
    # TODO: Start the shell
    while True:
        # print("CliReader:>",sep="\t")
        cmd = input("CliReader:> ")
        args = cmd.split()
        len_args = len(args)
        cmd_obj = cmdFactoryObj.get_command(args[0])
        rest = args[1:] if len_args != 1 else []
        status_code, result = cmd_obj.execute(rest)
        # print(status_code)

        # TODO: Result will be shown on some kind of UI so will call a method being made by arnab meanshile printing result on Standard Output
        # print(result)
