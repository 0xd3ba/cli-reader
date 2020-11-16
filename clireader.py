# clireader.py -- The entry point of the application

from __future__ import unicode_literals
import sys
import shell.cmdfactory as cmdfactory
from crawlers.cfactory import CrawlerFactory as cf
'''
following are the imports from prompt-tookit
for AutoSuggestion and World Completion and session
'''
from prompt_toolkit.styles import Style  # for styling the prompt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import PromptSession

PROMPT_USERNAME = 'clireader'
style = Style.from_dict({
    # User input (default text).
    '':          '#263238',

    # Prompt.
    'username': '#EACE6A',
    'at':       '#00aa00',
    'colon':    '#0000aa',
    'pound':    '#00aa00',
    'novelname':     '#00ffff',
    'path':     'ansicyan underline',
    'completion-menu.completion': 'bg:#008888 #ffffff',
    'completion-menu.completion.current': 'bg:#00aaaa #000000',
    'scrollbar.background': 'bg:#88aaaa',
    'scrollbar.button': 'bg:#222222',
})
PROMPT_NOVEL_INDEX = 2
prompt_message = [
    ['class:username', PROMPT_USERNAME],
    ['class:at',       '@'],
    ['class:novelname',     cf.DEFAULT_WEB],
    ['class:colon',    ':'],
]
command_completer = WordCompleter(
    ['help', 'listwebs', 'search', 'read', 'setweb', 'quit'])

if __name__ == '__main__':
    session = PromptSession()
    # Add new path variables
    sys.path.append('crawlers/')
    sys.path.append('shell/')

    cmdFactoryObj = cmdfactory.CommandFactory()
    # TODO: Start the shell
    while True:
        # print("CliReader:>",sep="\t")
        try:
            cmd = session.prompt(
                prompt_message, style=style, completer=command_completer, auto_suggest=AutoSuggestFromHistory())
        except KeyboardInterrupt:
            print("Use quit Command to quit the shell")
            continue
        except EOFError:
            break
        else:
            args = cmd.split()
            len_args = len(args)
            if len_args == 0:
                continue
            cmd_obj = cmdFactoryObj.get_command(args[0])
            rest = args[1:] if len_args != 1 else []
            status_code, result = cmd_obj.execute(rest)
        prompt_message[PROMPT_NOVEL_INDEX][-1] = cf.DEFAULT_WEB
        print(cf.DEFAULT_WEB)
        # print(status_code)

        # TODO: Result will be shown on some kind of UI so will call a method being made by arnab meanshile printing result on Standard Output
        # print(result)
