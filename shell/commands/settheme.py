# settheme.py -- Changes the theme B-)

import shell.cmdbase
import shell.format_utils.result_formatter as res_fmt

class SetThemeCommand(shell.cmdbase.CommandBase):
    """
    settheme -- Change the theme to the theme specifies
    Usage: settheme <theme_id>

    Example: settheme aqua-blue
    """
    DESCRIPTION   = 'Changes the theme to the theme specified'
    ERR_INV_THEME = 'The entered theme is an invalid theme ID!'
    ERR_NO_ARGS   = 'The following themes are supported currently:'
    THEME_SUCCESS = 'Changed theme successfully to: '

    def __init__(self):
        super().__init__()

    def help(self):
        return self.__doc__

    def execute(self, cmd_args):
        """ Simply swaps the theme index """
        if not cmd_args:
            return self.CMD_STATUS_ERROR, res_fmt.res_format_settheme(self.ERR_NO_ARGS)

        theme_id = cmd_args[0]
        if theme_id not in res_fmt.SUPP_THEMES.keys():
            return self.CMD_STATUS_ERROR, res_fmt.res_format_error(self.ERR_INV_THEME)

        # Else it means the theme is supported, change the theme to it
        # It's just a matter of switching between indices
        res_fmt.READER_FMT_STYLES_INDEX = res_fmt.SUPP_THEMES[theme_id]
        return self.CMD_STATUS_SUCCESS, res_fmt.res_format_generic(self.THEME_SUCCESS + theme_id)

    def _parse_args(self, cmd_args):
        # Parsing of arguments is not needed here
        pass

    def _parse_result(self, result):
        # Parsing of results is not needed here
        pass
