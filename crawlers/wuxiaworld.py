# wuxiaworld.py -- The crawler for WuxiaWorld website

from bs4 import BeautifulSoup

from crawlers.cbase              import CrawlerBase
from crawlers.cutils.fetcher     import fetch
from crawlers.cutils.chap_utils  import create_get_chapter_retval
from crawlers.cutils.chap_utils  import create_search_retval_i
from crawlers.cexceptions.exbase import CrawlerExceptionBase
import crawlers.cutils.chap_utils as cutils


class WuxiaWorldCrawler(CrawlerBase):
    BASE_URL   = "https://www.wuxiaworld.com/novel"  # The base URL for the website
    SEARCH_URL = "https://www.wuxiaworld.com/api/novels/search?query="  # The URL for searches

    # To use when no search results were found with the keyword
    SEARCH_EMPTY_MSG = "No search results found with the following keyword: "
    NO_NEXT_CHAP_MSG = "There is no next chapter (yet), the current one is the latest one"
    NO_PREV_CHAP_MSG = "There is no previous chapter prior to this chapter"

    # The following are the keys of the parsed JSON object
    JSON_ITEM_KEY     = 'items'  # Where the search results are stored
    JSON_NOV_ABBR     = 'abbreviation'  # Short form of the novel (required for forming the URL)
    JSON_NOV_NAME     = 'name'
    JSON_NOV_SLUG     = 'slug'
    JSON_NOV_SYNP     = 'synopsis'
    JSON_NOV_TAGS     = 'tags'
    JSON_NOV_GENRES   = 'genres'
    JSON_NOV_CHAP_CNT = 'chapterCount'

    def __init__(self, novel_name, chap_num=None):
        self.novel = novel_name             # Name of the novel
        self.chapter = chap_num             # Chapter number of the novel to get
        self.novel_info = None              # Search result of the novel
        self.novel_slug = None              # The slug of the novel
        self.novel_abbr = None              # Short form of the novel
        self.novel_next_chap_slug = None    # The slug of next chapter
        self.novel_prev_chap_slug = None    # The slug of the previous chapter

    def get_chapter(self, chp_num):
        """
        Fetches the chapter numbered `chp_num` if it exists
        """
        novel_info = []
        chapter_html_resp = None

        status, novel_info = self.search()
        if status == self.CRAWLER_STATUS_ERR:
            # This means error occurred during search and novel_info contains the error message
            # No further processing can be done - Just return what it got
            return status, novel_info

        if len(novel_info) > 1:
            # If more than one novel turned up with the given search result
            # It means the keyword entered by user was not a good filter, indicate that the
            # get_chapter found more than one result in the status code and return the
            # results that were obtained from the search
            return self.CRAWLER_GET_MULT_RES, novel_info

        # It means the novel has been found, prepare the URL for the chapter
        # Then fetch the HTML file of the chapter
        curr_chap_url = self._prepare_novel_chapter_url(chp_num)

        # Fetch the contents of the chapter (if valid) along with the status code of the
        # operation
        status, contents = self._chapter_content_fetcher(self, chp_num, curr_chap_url)
        return status, contents

    def next_chapter(self):
        """
        Fetches the next chapter of the novel and returns a new crawler instance
        along with the chapter contents
        """
        if self.novel_next_chap_slug is None:
            return self.CRAWLER_STATUS_ERR, self.NO_NEXT_CHAP_MSG, None

        # The next chapter slug is not None, create a new instance of this crawler
        # And fill it with the common details
        next_chap_obj = self._create_new_instance()

        # Next chapter slug combined with base URL gives the chapter URL
        # This one is different from what get_chapter(...) needs to do
        next_chap_url = self._prepare_novel_url(self.novel_next_chap_slug)
        next_chap_num = self._extract_chap_num(self.novel_next_chap_slug)

        # Alright, fetch the contents
        status, contents = self._chapter_content_fetcher(next_chap_obj, next_chap_num, next_chap_url)
        return status, contents, next_chap_obj


    def previous_chapter(self):
        """
        Fetches the next chapter of the novel and returns a new crawler instance
        along with the chapter contents
        """
        if self.novel_prev_chap_slug is None:
            return self.CRAWLER_STATUS_ERR, self.NO_PREV_CHAP_MSG, None

        # The prev chapter slug is not None, create a new instance of this crawler
        # And fill it with the common details
        prev_chap_obj = self._create_new_instance()

        # Prev chapter slug combined with base URL gives the chapter URL
        prev_chap_url = self._prepare_novel_url(self.novel_prev_chap_slug)
        prev_chap_num = self._extract_chap_num(self.novel_prev_chap_slug)

        # Alright, fetch the contents
        status, contents = self._chapter_content_fetcher(prev_chap_obj, prev_chap_num, prev_chap_url)
        return status, contents, prev_chap_obj


    def search(self):
        # Step-1: Get the homepage of the novel
        try:
            search_resp = fetch(self._prepare_search_url())
        except CrawlerExceptionBase as crex:
            err_msg = crex.handler()
            return self.CRAWLER_STATUS_ERR, err_msg

        results = self._parse_json_resp(search_resp)  # Parse the JSON file contents

        # No search result with the following keyword
        if not results:
            err_msg = self.SEARCH_EMPTY_MSG + self.novel
            return self.CRAWLER_STATUS_ERR, err_msg

        return self.CRAWLER_STATUS_OK, results

    # ---------- Private helper methods ---------- #

    def _create_new_instance(self):
        """
        Creates a new instance of this class, duplicates the instance variables
        that are shared across the same novel
        """
        new_obj = WuxiaWorldCrawler(self.novel)
        new_obj.novel_info = self.novel_info
        new_obj.novel_slug = self.novel_slug
        new_obj.novel_abbr = self.novel_abbr
        return new_obj

    def _prepare_novel_url(self, slug):
        return f'{self.BASE_URL}/{slug}'

    def _prepare_novel_chapter_url(self, chap_num):
        """
        Novel chapter URLs in Wuxiaworld are of the form:
        /<slug>/<abbreviation>-chapter-<num>
        """
        slug = self.novel_slug
        abbr = self.novel_abbr.lower()
        nurl = self._prepare_novel_url(slug)
        nov_chp_url = nurl + f'/{abbr}-chapter-{str(chap_num)}'

        return nov_chp_url

    def _prepare_search_url(self):
        """
        Prepare a search URL given the name of the novel
        """
        query = self.novel.split(' ')  # Split at space characters
        query = '%20'.join(query)  # Replace with "%20"
        return self.SEARCH_URL + query  # Append with search query URL and return

    def _extract_chap_num(self, chap_slug):
        """
        Extracts the chapter number from the slug. There are some cases when the novel's
        chapter number is a fricking decimal number, so incrementing/decrementing chapter
        number by one won't cut it

        /novel/<novel_name>/<novel_abbr>-chapter-<number>-<decimal_1>-<decimal_2>- ...
        """
        chap_num = chap_slug.split('/')[-1]      # The last part: <novel_abbr>-chapter-<number>-<decimal_1>- ...
        chap_num = chap_num.split('-')[2:]       # The chapter number part: <number>-<decimal_1>-
        chap_num = '-'.join(chap_num)
        return chap_num

    def _set_next_prev_slugs(self, next_slug, prev_slug):
        """
        Sets the slugs of next and previous chapter relative to the current chapter
        """
        self.novel_next_chap_slug = next_slug
        self.novel_prev_chap_slug = prev_slug

    def _parse_json_resp(self, json_response):
        """
        Wuxiaworld searches returns a JSON file. Parse it to a list of dictionaries
        """
        search_res = []
        meta_info_res = []        # To store some meta information about the novel (slug & abbreviation)
        json_obj = json_response.json()

        META_INFO_RES_SLUG_IDX = 0
        META_INFO_RES_ABBR_IDX = 1

        # For each result, only keep the necessary information
        for nov_info in json_obj[self.JSON_ITEM_KEY]:

            novel_i_name     = nov_info[self.JSON_NOV_NAME]
            novel_i_slug     = nov_info[self.JSON_NOV_SLUG]
            novel_i_tags     = nov_info[self.JSON_NOV_TAGS]
            novel_i_chap_cnt = nov_info[self.JSON_NOV_CHAP_CNT]
            novel_i_genres   = nov_info[self.JSON_NOV_GENRES]
            novel_i_abbr     = nov_info[self.JSON_NOV_ABBR]
            novel_i_synp     = self._get_paragraphs(nov_info[self.JSON_NOV_SYNP])

            # Finally save this result to the list of results
            novel_i = create_search_retval_i(novel_name=novel_i_name,
                                             chap_count=novel_i_chap_cnt,
                                             synopsis=novel_i_synp,
                                             tags=novel_i_tags,
                                             genres=novel_i_genres)
            search_res.append(novel_i)
            meta_info_res.append([novel_i_slug, novel_i_abbr])

        # If we filtered out the novel we wanted, save the information about it
        if len(search_res) == 1:
            self.novel = search_res[0][cutils.SEARCH_NOV_NAME_KEY]
            self.novel_info = search_res[0]
            self.novel_slug = meta_info_res[0][META_INFO_RES_SLUG_IDX]
            self.novel_abbr = meta_info_res[0][META_INFO_RES_ABBR_IDX]

        return search_res

    def _get_paragraphs(self, html_file):
        """
        Given contents of a HTML file, return the paragraphs from it
        """

        # TODO: Apply a strict filter to prevent things other than chapters from coming up

        paras = []
        bs_obj = BeautifulSoup(html_file, self.DEFAULT_HTML_PARSER)
        paras_tags = bs_obj.find_all('p')  # A list of BeautifulSoup Tag objects

        # Convert all the paragraphs to text and append to the list of paragraphs
        for ptag in paras_tags:
            paras.append(ptag.get_text().strip())

        return paras

    def _get_next_prev_slugs(self, html_file):
        """
        Extract the slugs to next and previous chapters from the current HTML file
        Previous Slug:  <link rel="prev" href="the-slug-of-previous-chapter">
        Next Slug:      <link rel="next" href="the-slug-of-next-chapter">
        """
        next_slug = None
        prev_slug = None

        target_tag   = 'link'
        target_loc   = 'href'
        next_var_val = 'next'
        prev_var_val = 'prev'
        attr_var     = 'rel'
        target_attrs = {attr_var: None}

        bs_obj = BeautifulSoup(html_file, self.DEFAULT_HTML_PARSER)

        # Step-1: Find the slug of previous chapter, if any
        target_attrs[attr_var] = prev_var_val
        prev_slug_tag = bs_obj.find_all(target_tag, attrs=target_attrs)
        if prev_slug_tag:
            prev_slug = prev_slug_tag[0][target_loc]
            # Now remove the /novel/ part from the slug because the base URL already has it
            prev_slug = prev_slug.split('/')[2:]
            prev_slug = '/'.join(prev_slug)

        # Step-2: Find the slug of the next chapter, if any
        target_attrs[attr_var] = next_var_val
        next_slug_tag = bs_obj.find_all(target_tag, attrs=target_attrs)
        if next_slug_tag:
            next_slug = next_slug_tag[0][target_loc]
            # Now remove the /novel/ part from the slug because the base URL already has it
            next_slug = next_slug.split('/')[2:]
            next_slug = '/'.join(next_slug)

        return next_slug, prev_slug

    def _chapter_content_fetcher(self, new_self, chp_num, chap_url):
        """
        Fetches the chapter contents, sets the next/prev slugs (if any)
        and returns with status code and the contents/error message

        new_self is another instance of this class - Using this to unify
        next_chapter/prev_chapter along with get_chapter(...) methods
        """
        try:
            chapter_html_resp = fetch(chap_url)
        except CrawlerExceptionBase as crex:
            err_msg = crex.handler()
            return new_self.CRAWLER_STATUS_ERR, err_msg

        # Chapter contents -- A list of chapter paragraphs
        chapter_conts = new_self._get_paragraphs(chapter_html_resp.text)

        # Extract the URLs to next and previous chapters, if any
        # If any of them doesn't exist, their values are None
        next_slug, prev_slug = new_self._get_next_prev_slugs(chapter_html_resp.text)
        new_self._set_next_prev_slugs(next_slug, prev_slug)

        # Name of the novel was already updated in the JSON parsing method
        # Prepare the dictionary to return
        parsed_retval = create_get_chapter_retval(self.novel,
                                                  chp_num,
                                                  chapter_conts,
                                                  title=None
                                                  )

        return new_self.CRAWLER_STATUS_OK, parsed_retval