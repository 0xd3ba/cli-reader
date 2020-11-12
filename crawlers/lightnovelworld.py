# lightnovelworld.py -- The crawler for LightNovelWorld website

from bs4 import BeautifulSoup

from crawlers.cbase              import CrawlerBase
from crawlers.cutils.fetcher     import fetch
from crawlers.cutils.chap_utils  import create_get_chapter_retval
from crawlers.cexceptions.exbase import CrawlerExceptionBase


class LightNovelWorldCrawler(CrawlerBase):
    BASE_URL   = "https://www.lightnovelworld.com"                              # The base URL for the website
    SEARCH_URL = "https://www.lightnovelworld.com/lnwsearchlive?inputContent="  # The URL for searches

    # To use when no search results were found with the keyword
    SEARCH_EMPTY_MSG = "No search results found with the following keyword: "

    JSON_ITEM_KEY = 'resultview'    # The results of the searches are stored with this key
    JSON_NOV_NAME = 'name'
    JSON_NOV_SLUG = 'slug'
    JSON_NOV_CHAP_CNT = 'chapterCount'

    def __init__(self, novel_name, chap_num=None):
        self.novel = novel_name
        self.chapter = chap_num
        self.novel_info = None

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
        novel_curr_chp_url = self._prepare_novel_chapter_url(novel_info[0], chp_num)
        try:
            chapter_html_resp = fetch(novel_curr_chp_url)
        except CrawlerExceptionBase as crex:
            err_msg = crex.handler()
            return self.CRAWLER_STATUS_ERR, err_msg

        # Chapter contents -- A list of chapter paragraphs
        chapter_conts = self._get_paragraphs(chapter_html_resp.text)

        # Extract the URLs to next and previous chapters, if any
        # If any of them doesn't exist, their values are None
        next_slug, prev_slug = self._get_next_prev_slugs(chapter_html_resp.text)

        # Name of the novel was already updated in the JSON parsing method
        # Prepare the dictionary to return
        parsed_retval = create_get_chapter_retval(self.novel,
                                                  chp_num,
                                                  chapter_conts,
                                                  title=None,
                                                  next_slug=next_slug,
                                                  prev_slug=prev_slug)

        return self.CRAWLER_STATUS_OK, parsed_retval

    def next_chapter(self):
        # TODO: Fetch the next chapter, if any
        pass

    def previous_chapter(self):
        # TODO: Fetch the previous chapter, if any
        pass

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

    def get_summary(self, novel_name):
        pass

    # ---------- Private helper methods ---------- #

    def _prepare_novel_url(self, slug):
        return f'{self.BASE_URL}{slug}'

    def _prepare_novel_chapter_url(self, novel_info, num):
        """
        Novel chapter URLs in Wuxiaworld are of the form:
        /<slug>/chapter-<num>
        """
        slug = novel_info[self.JSON_NOV_SLUG]
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

            novel_i[self.JSON_NOV_NAME]     = nov_title
            novel_i[self.JSON_NOV_SLUG]     = nov_slug
            novel_i[self.JSON_NOV_CHAP_CNT] = nov_chps

            # Finally save this result to the list of resuts
            search_res.append(novel_i)

        # If we filtered out the novel we wanted, save the information about it
        if len(search_res) == 1:
            self.novel = search_res[0][self.JSON_NOV_NAME]
            self.novel_info = search_res[0]

        return search_res

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

        bs_obj = BeautifulSoup(html_file, self.DEFAULT_HTML_PARSER)

        # Step-1: Find the slug of previous chapter, if any
        target_attrs[attr_var] = prev_var_val
        prev_slug_tag = bs_obj.find(target_tag, attrs=target_attrs)
        if prev_slug_tag:
            prev_slug = prev_slug_tag[target_loc]

        # Step-2: Find the slug of the next chapter, if any
        target_attrs[attr_var] = next_var_val
        next_slug_tag = bs_obj.find_all(target_tag, attrs=target_attrs)
        if next_slug_tag:
            next_slug = next_slug_tag[0][target_loc]

        return next_slug, prev_slug
