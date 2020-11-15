# lightnovelworld.py -- The crawler for LightNovelWorld website

from bs4 import BeautifulSoup

from crawlers.cbase              import CrawlerBase
from crawlers.cutils.fetcher     import fetch
from crawlers.cutils.chap_utils  import create_get_chapter_retval
from crawlers.cutils.chap_utils  import create_search_retval_i
from crawlers.cexceptions.exbase import CrawlerExceptionBase

import crawlers.cutils.chap_utils as cutils


class LightNovelWorldCrawler(CrawlerBase):
    BASE_URL   = "https://www.lightnovelworld.com"                              # The base URL for the website
    SEARCH_URL = "https://www.lightnovelworld.com/lnwsearchlive?inputContent="  # The URL for searches

    JSON_ITEM_KEY = 'resultview'    # The results of the searches are stored with this key
    JSON_NOV_NAME = 'name'
    JSON_NOV_SLUG = 'slug'
    JSON_NOV_CHAP_CNT = 'chapterCount'

    def __init__(self, novel_name, chap_num=None):
        self.novel = novel_name
        self.chapter = chap_num
        self.novel_info = None            # Search result of the novel
        self.novel_slug = None            # The slug of the novel
        self.novel_abbr = None            # Short form of the novel
        self.novel_next_chap_slug = None  # The slug of next chapter
        self.novel_prev_chap_slug = None  # The slug of the previous chapter

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
        curr_chap_url = self._prepare_novel_chapter_url(novel_info[0], chp_num)

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
        new_obj = LightNovelWorldCrawler(self.novel)
        new_obj.novel_info = self.novel_info
        new_obj.novel_slug = self.novel_slug
        new_obj.novel_abbr = self.novel_abbr
        return new_obj

    def _prepare_novel_url(self, slug):
        return f'{self.BASE_URL}{slug}'

    def _prepare_novel_chapter_url(self, novel_info, num):
        """
        Novel chapter URLs in Wuxiaworld are of the form:
        /<slug>/chapter-<num>
        """
        slug = self.novel_slug
        nurl = self._prepare_novel_url(slug)
        nov_chp_url = nurl + f'/chapter-{str(num)}'

        return nov_chp_url

    def _prepare_search_url(self):
        """
        Prepare a search URL given the name of the novel
        """
        query = self.novel.split(' ')  # Split at space characters
        query = '%20'.join(query)  # Replace with "%20"
        return self.SEARCH_URL + query  # Append with search query URL and return

    def _parse_json_resp(self, json_response):
        """
        Lightnovelworld searches returns a JSON file. Parse it to a list of dictionaries
        """
        # The search results are placed inside <li>...</li> tags with attribute "class = novel-item"
        # 1. The slug of the novel is inside <a>...</a> tag's "href" attribute
        # 2. The title of the novel is inside <a>...</a> tag's "title" attribute
        # 3. The number of chapters is inside <span>...</span> tag of the form "xyz Chapters"
        #    (The first word is the number of chapters)

        search_tags    = 'li'
        titl_slug_tags = 'a'
        chp_count_tags = 'span'
        search_attrs   = {'class':'novel-item'}
        title_attrs    = 'title'
        slug_attrs     = 'href'

        search_res = []
        meta_info_res = []

        json_content = json_response.json()[self.JSON_ITEM_KEY]
        bsobj = BeautifulSoup(json_content, self.DEFAULT_HTML_PARSER)

        search_res_tags = bsobj.find_all(search_tags, search_attrs)

        # For each result, only extract and keep the necessary information
        for nov_info_tag in search_res_tags:
            novel_i = {}

            titl_slug_tag = nov_info_tag.find(titl_slug_tags)
            chp_count_tag = nov_info_tag.find(chp_count_tags)

            nov_title = titl_slug_tag[title_attrs]
            nov_slug  = titl_slug_tag[slug_attrs]
            nov_chps  = chp_count_tag.get_text().strip().split(' ')[0]

            novel_i = create_search_retval_i(novel_name=nov_title,
                                             chap_count=nov_chps,
                                             )
            search_res.append(novel_i)
            meta_info_res.append(nov_slug)

        # If we filtered out the novel we wanted, save the information about it
        if len(search_res) == 1:
            self.novel = search_res[0][cutils.SEARCH_NOV_NAME_KEY]
            self.novel_info = search_res[0]
            self.novel_slug = meta_info_res[0]

        return search_res

    def _set_next_prev_slugs(self, next_slug, prev_slug):
        """
        Sets the slugs of next and previous chapter relative to the current chapter
        """
        self.novel_next_chap_slug = next_slug
        self.novel_prev_chap_slug = prev_slug

    def _extract_chap_num(self, chap_slug):
        """
        Extracts the chapter number from the slug. There are some cases when the novel's
        chapter number is a fricking decimal number, so incrementing/decrementing chapter
        number by one won't cut it

        /novel/<novel_name>/chapter-<number>-<decimal_1>-<decimal_2>- ...
        """
        chap_num = chap_slug.split('/')[-1]      # The last part: chapter-<number>-<decimal_1>- ...
        chap_num = chap_num.split('-')[1:]       # The chapter number part: <number>-<decimal_1>-
        chap_num = '-'.join(chap_num)
        return chap_num

    def _get_paragraphs(self, html_file):
        """
        Given contents of a HTML file, return the paragraphs from it
        """

        # The chapter contents are present inside <div>...</div> tags
        # with attribute "class = chapter-content"
        # Within it, the actual contents are within paragraph <p>...</p>
        # tags

        class_cont_tags  = 'div'
        class_cont_attrs = {'class': 'chapter-content'}
        chap_cont_tags   = 'p'

        paras = []
        bs_obj = BeautifulSoup(html_file, self.DEFAULT_HTML_PARSER)
        cont_tags = bs_obj.find(class_cont_tags, attrs=class_cont_attrs)
        paras_tags = cont_tags.find_all(chap_cont_tags)

        for ptag in paras_tags:
            paras.append(ptag.get_text().strip())

        # This is the case when filtering by <p> tags was not successful
        # This happens when the text is placed with only <br/> tags -- Need a different
        # approach
        # Extract the strings inside the container, then append them to the paras list
        if not paras_tags:
            string_list = cont_tags.strings
            for string in string_list:
                paras.append(string.strip())

        return paras

    def _get_next_prev_slugs(self, html_file):
        """
        Extract the slugs to next and previous chapters from the current HTML file
        Previous Slug:  <a class="prevchap" href="the-slug-of-previous-chapter">
        Next Slug:      <a class="nextchap" href="the-slug-of-next-chapter">
        """
        next_slug = None
        prev_slug = None

        target_tag   = 'a'
        target_loc   = 'href'
        next_var_val = 'nextchap'
        prev_var_val = 'prevchap'
        attr_var     = 'class'
        target_attrs = {attr_var: None}

        title_attr = 'title'
        not_avail = 'No Chapter Available' # Chapter title is this value if it's not present

        bs_obj = BeautifulSoup(html_file, self.DEFAULT_HTML_PARSER)

        # Step-1: Find the slug of previous chapter, if any
        target_attrs[attr_var] = prev_var_val
        prev_slug_tag = bs_obj.find(target_tag, attrs=target_attrs)
        if prev_slug_tag:
            prev_slug = prev_slug_tag[target_loc]
            if prev_slug_tag[title_attr] == not_avail:
                prev_slug = None

        # Step-2: Find the slug of the next chapter, if any
        target_attrs[attr_var] = next_var_val
        next_slug_tag = bs_obj.find(target_tag, attrs=target_attrs)
        if next_slug_tag:
            next_slug = next_slug_tag[target_loc]
            if next_slug_tag[title_attr] == not_avail:
                next_slug = None

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