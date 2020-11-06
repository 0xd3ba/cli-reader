# chap_utils.py -- Contains all the common utility methods required by the
#                  crawler to handle novel chapters

GET_CHAP_NOV_NAME_KEY = 'novel_title'
GET_CHAP_CONTENTS_KEY = 'contents'
GET_CHAP_TITLE_KEY = 'chap_title'
GET_CHAP_NEXT_SLUG_KEY = 'next_slug'
GET_CHAP_PREV_SLUG_KEY = 'prev_slug'
GET_CHAP_DEFAULT_TITLE = 'Chapter-'

def create_get_chapter_retval(novel_name, chap_num, paragraphs, title=None, next_slug=None, prev_slug=None):
    """
    Creates the return value dictionary that `get_chapter(...)` of the crawler
    needs to return
    """
    if title is None:
        title = GET_CHAP_DEFAULT_TITLE + str(chap_num)

    get_chap_dict = {GET_CHAP_NOV_NAME_KEY: novel_name, # The name of the novel
                     GET_CHAP_TITLE_KEY: title,         # The title of the chapter
                     GET_CHAP_CONTENTS_KEY: paragraphs, # The list of paragraphs
                     GET_CHAP_NEXT_SLUG_KEY: next_slug,   # The slug (i.e. location) of the next chapter
                     GET_CHAP_PREV_SLUG_KEY: prev_slug    # The slug of the previous chapter
                     }

    return get_chap_dict