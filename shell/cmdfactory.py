# cmdfactory.py -- Contains the factory class for all the supported commands

import shell.commands.defcmd   as defcmd
import shell.commands.addfav   as addfav
import shell.commands.help     as help
import shell.commands.listwebs as listwebs
import shell.commands.listfav  as listfav
import shell.commands.read     as read
import shell.commands.rmfav    as rmfav
import shell.commands.setweb   as setweb
import shell.commands.search   as search
import shell.commands.quit     as quit

class CommandFactory:
    """
    CommandFactory -- Factory class for returning command objects to the shell
    """

    # Store the references of each class according to command name
    DEF_CMD = defcmd.DefaultCommand             # Default command that's executed when user enters an invalid command
    SUPPORTED_CMDS = {
        'addfav':   addfav.AddFavoritesCommand, # Add the current novel to favorites
        'help':     help.HelpCommand,           # Display information about the command
        'listwebs': listwebs.ListWebsCommand,   # List the supported websites
        'listfav':  listfav.ListFavCommand,     # List all the favorites
        'read':     read.ReadCommand,           # Read the specified novel
        'rmfav':    rmfav.RemFavCommand,        # Remove from favorites
        'setweb':   setweb.SetWebCommand,       # Set the default website to use
        'search':   search.SearchCommand,       # Search novel in a website (if specified), else use default website
        'quit':     quit.QuitCommand            # Exit the shell
    }

    def get_command(self, cmd):
        """
        Returns an appropriate command object according to the `cmd` argument
        """
        if cmd not in self.SUPPORTED_CMDS:
            return self.DEF_CMD()

        # Command is a valid command, return the corresponding object
        return self.SUPPORTED_CMDS[cmd]()