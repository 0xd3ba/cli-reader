# result_formatter.py -- Formats the results of the commands that needs to return output

import prompt_toolkit as ptk


HEADER_COLOR    = '#29b6f6'
NORMAL_COLOR    = '#fafafa'
HIGHLIGHT_COLOR = '#fdd835'

HEADER_TEXT_STYLE    = 'italic'
NORMAL_TEXT_STYLE    = ''
HIGHLIGHT_TEXT_STYLE = ''

# Border to separate header from data
DATA_SEP_CHAR = '-'

# The style dictionary to use for styling
FMT_STYLES = {
    'header':    f'{HEADER_COLOR} {HEADER_TEXT_STYLE}',
    'normal':    f'{NORMAL_COLOR} {NORMAL_TEXT_STYLE}',
    'highlight': f'{HIGHLIGHT_COLOR} {HIGHLIGHT_TEXT_STYLE}'
}

FMT_STYLES_HDR_KEY = 'header'
FMT_STYLES_NRM_KEY = 'normal'
FMT_STYLES_HL_KEY  = 'highlight'


def res_format_listwebs(webids, webnames, header_idcol, header_webcol):
    """ Result formatter for listwebs command """

    ljust_len = max([len(wb) for wb in webnames])
    rjust_len = ljust_len

    webids_lj = [wid.ljust(ljust_len) for wid in webids]
    webnam_rj = [wnm.rjust(rjust_len) for wnm in webnames]

    # Here's the thing, the IDs need a separate entry (to highlight each individually)
    # Same goes for the website name -- A separate entry, so need twice more entries
    # Need 2 extra for header row and the row for data separator
    fmt_list  = [None for _ in range(len(webids)*2 + 2)]

    # Format the header and the separator first
    header_str   = header_idcol.ljust(ljust_len) + header_webcol.rjust(rjust_len) + '\n'
    data_sep_str = DATA_SEP_CHAR * (ljust_len + rjust_len) + '\n'

    fmt_list[0] = (FMT_STYLES[FMT_STYLES_HDR_KEY], header_str)
    fmt_list[1] = (FMT_STYLES[FMT_STYLES_HDR_KEY], data_sep_str)

    # Skip in twos, 'i' for Website Identifier
    # 'i+1' for website name
    for i in range(2, len(fmt_list), 2):
        fmt_list[i]   = (FMT_STYLES[FMT_STYLES_HL_KEY], webids_lj[i//2 - 1])
        fmt_list[i+1] = (FMT_STYLES[FMT_STYLES_NRM_KEY], webnam_rj[i//2 - 1] + '\n')

    # By now we have a formatted list ready
    # Feed it to FormattedText to get the formatted text object we need to return
    fmt_obj = ptk.formatted_text.FormattedText(fmt_list)
    return fmt_obj


def res_format_search():
    """ Result formatter for search command """
    pass