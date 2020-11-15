# chap_utils.py -- Contains all the common utility methods required by the
#                  crawler to handle novel chapters

GET_CHAP_NOV_NAME_KEY = 'novel_title'
GET_CHAP_CONTENTS_KEY = 'contents'
GET_CHAP_TITLE_KEY = 'chap_title'
GET_CHAP_DEFAULT_TITLE = 'Chapter-'

# Writing them prettily because they will be printed to the screen
SEARCH_NOV_NAME_KEY = 'Title'
SEARCH_NOV_SYNP_KEY = 'Synopsis'
SEARCH_NOV_TAGS_KEY = 'Tags'
SEARCH_NOV_GENRES_KEY = 'Genres'
SEARCH_NOV_CHAP_CNT_KEY = 'Chapter Count'


def create_get_chapter_retval(novel_name, chap_num, paragraphs, title=None):
    """
    Creates the return value dictionary that `get_chapter(...)` of the crawler
    needs to return
    """
    if title is None:
        title = GET_CHAP_DEFAULT_TITLE + str(chap_num)

    get_chap_dict = {GET_CHAP_NOV_NAME_KEY: novel_name,   # The name of the novel
                     GET_CHAP_TITLE_KEY: title,           # The title of the chapter
                     GET_CHAP_CONTENTS_KEY: paragraphs,   # The list of paragraphs
                     }

    return get_chap_dict


def create_search_retval_i(novel_name, chap_count=None, synopsis=None, tags=None, genres=None):
    """
    Creates a dictionary of the i'th novel of the search result
    """
    search_res_i = {SEARCH_NOV_NAME_KEY: novel_name,      # Name of the novel
                    SEARCH_NOV_CHAP_CNT_KEY: chap_count,  # Number of chapters of the novel currently
                    SEARCH_NOV_SYNP_KEY: synopsis,        # Synopsis of the novel
                    SEARCH_NOV_TAGS_KEY: tags,            # Tags of the novel
                    SEARCH_NOV_GENRES_KEY: genres         # Genre of the novel
                    }

    return search_res_i
