# result_formatter.py -- Formats the results of the commands that needs to return output

import crawlers.cutils.chap_utils as chap_utils
import prompt_toolkit as ptk


HEADER_COLOR    = '#29b6f6'
NORMAL_COLOR    = '#fafafa'
HIGHLIGHT_COLOR = '#fdd835'
ERROR_COLOR     = '#f4511e'

HEADER_TEXT_STYLE    = 'italic'
ERROR_TEXT_STYLE     = ''
NORMAL_TEXT_STYLE    = ''
HIGHLIGHT_TEXT_STYLE = ''

# Border to separate header from data
DATA_SEP_CHAR = '-'

# Search result message header
SEARCH_RES_HDR = 'Number of results found: '

# The style dictionary to use for styling
FMT_STYLES = {
    'header':    f'{HEADER_COLOR} {HEADER_TEXT_STYLE}',
    'normal':    f'{NORMAL_COLOR} {NORMAL_TEXT_STYLE}',
    'highlight': f'{HIGHLIGHT_COLOR} {HIGHLIGHT_TEXT_STYLE}',
    'error':     f'{ERROR_COLOR} {ERROR_TEXT_STYLE}'
}

FMT_STYLES_HDR_KEY = 'header'
FMT_STYLES_NRM_KEY = 'normal'
FMT_STYLES_HL_KEY  = 'highlight'
FMT_STYLES_ERR_KEY = 'error'


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


def res_format_search(search_results, keyword):
    """ Result formatter for search command """

    # First find out how many keys we need to accommodate -- This can be
    # done by looping through the first result (guaranteed to be at least one)
    # and checking how many keys have the value NONE. Remove these entries
    # from the search results
    inval_keys = []
    num_search_res = len(search_results)

    for key, val in search_results[0].items():
        if val is None:
            inval_keys.append(key)

    # Now for all entries in the search result, delete the invalid keys
    for i in range(num_search_res):
        for inv_key in inval_keys:
            del search_results[i][inv_key]


    # By now all the invalid keys are gone :)
    num_keys = len(search_results[0])
    val_keys = search_results[0].keys()

    ljust_len = max([len(k) for k in val_keys]) + 4

    search_header_msg = SEARCH_RES_HDR + f'{num_search_res} ({keyword})'
    res_separator = DATA_SEP_CHAR * ljust_len * 2

    # Tricky calculation
    # There are a total of `num_search_res` results, each with `num_keys` key-value pairs
    # Need a total of `num_search_res` spacings (one extra for last entry)
    # Need 1 extra for `search_header_msg`

    num_spacings = num_search_res
    fmt_list = [None for _ in range(num_search_res*num_keys*2 + num_spacings + 1)]

    fmt_list[0] = (FMT_STYLES[FMT_STYLES_HDR_KEY], search_header_msg + '\n\n')
    fmt_lidx = 1

    for search_res in search_results:
        for key, val in search_res.items():
            fmt_list[fmt_lidx] = (FMT_STYLES[FMT_STYLES_HL_KEY], key.ljust(ljust_len))

            # Convert value to a string if it is a list
            val = '  '.join(val) if isinstance(val, list) else val
            fmt_list[fmt_lidx+1] = (FMT_STYLES[FMT_STYLES_NRM_KEY], str(val) + '\n')

            fmt_lidx += 2

        # End of result 1, insert double spaces to separate this from next entry
        fmt_list[fmt_lidx] = (FMT_STYLES[FMT_STYLES_NRM_KEY], '\n' + res_separator + '\n\n')
        fmt_lidx += 1

    # The formatted text list is filled
    # Return a FormattedText object to the caller
    return ptk.formatted_text.FormattedText(fmt_list)

def res_format_error(msg):
    """ Result formatter for error messages """

    err_msg = 'ERROR: ' + msg
    fmt_msg = [(FMT_STYLES[FMT_STYLES_ERR_KEY], err_msg)]
    fmt_obj = ptk.formatted_text.FormattedText(fmt_msg)

    return fmt_obj