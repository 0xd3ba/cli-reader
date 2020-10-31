# wuxiaworld.py -- The crawler for WuxiaWorld website

from bs4                        import BeautifulSoup
from crawlers.cbase             import CrawlerBase
from crawlers.cutils.fetcher    import fetch
from crawlers.cutils.chap_utils import create_get_chapter_retval


class WuxiaWorldCrawler(CrawlerBase):
    BASE_URL   = "https://www.wuxiaworld.com/novel"  # The base URL for the website
    SEARCH_URL = "https://www.wuxiaworld.com/api/novels/search?query="  # The URL for searches

    # The following are the keys of the parsed JSON object
    JSON_ITEM_KEY     = 'items'  # Where the search results are stored
    JSON_NOV_ABBR     = 'abbreviation'  # Short form of the novel (required for forming the URL)
    JSON_NOV_NAME     = 'name'
    JSON_NOV_SLUG     = 'slug'
    JSON_NOV_SUMM     = 'synopsis'
    JSON_NOV_TAGS     = 'tags'
    JSON_NOV_GENRES   = 'genres'
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

        try:
            novel_info = self.search()
        except Exception as e:  # For now simply catch a generic exception (fetching error, no search results)
            #TODO: Update the exception handling
            pass

        if len(novel_info) > 1:
            # If more than one novel turned up with the given search result
            # Throw an exception indicating that more than one novel was found
            # Print the search results as well -- user will give a request again depending on this
            # TODO: Do the above commented stuff
            pass

        # It means the novel has been found, prepare the URL for the chapter
        # Then fetch the HTML file of the chapter
        novel_curr_chp_url = self._prepare_novel_chapter_url(novel_info[0], chp_num)
        try:
            chapter_html_resp = fetch(novel_curr_chp_url)
        except Exception as e:
            # TODO: Handle fetching exceptions if any
            pass

        # Chapter contents -- A list of chapter paragraphs
        chapter_conts = self._get_paragraphs(chapter_html_resp.text)

        # Extract the URLs to next and previous chapters, if any
        # If any of them doesn't exist, their values are None
        next_url, prev_url = self._get_next_prev_urls(chapter_html_resp.text)

        # Name of the novel was already updated in the JSON parsing method
        # Prepare the dictionary to return
        parsed_retval = create_get_chapter_retval(self.novel,
                                                  chp_num,
                                                  chapter_conts,
                                                  title=None,
                                                  next_url=next_url,
                                                  prev_url=prev_url)

        return parsed_retval

    def next_chapter(self):
        # TODO: Fetch the next chapter, if any
        pass

    def previous_chapter(self):
        # TODO: Fetch the previous chapter, if any
        pass

    def search(self):
        # Step-1: Get the homepage of the novel
        search_resp = fetch(self._prepare_search_url())
        if search_resp is None:
            # TODO: Fetching error, already logged the error
            # Raise an exception
            pass
        else:
            results = self._parse_json_resp(search_resp)  # Parse the JSON file contents
            if not results:
                # TODO: No search results -- Raise novel not found exception
                pass
            return results

    def get_summary(self, novel_name):
        pass

    # ---------- Private helper methods ---------- #

    def _prepare_novel_url(self, slug):
        return f'{self.BASE_URL}/{slug}'

    def _prepare_novel_chapter_url(self, novel_info, num):
        """
        Novel chapter URLs in Wuxiaworld are of the form:
        /<slug>/<abbreviation>-chapter-<num>
        """
        slug = novel_info[self.JSON_NOV_SLUG]
        abbr = novel_info[self.JSON_NOV_ABBR].lower()
        nurl = self._prepare_novel_url(slug)
        nov_chp_url = nurl + f'/{abbr}-chapter-{str(num)}'

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
        Wuxiaworld searches returns a JSON file. Parse it to a list of dictionaries
        """
        search_res = []
        json_obj = json_response.json()

        # For each result, only keep the necessary information
        for nov_info in json_obj[self.JSON_ITEM_KEY]:
            novel_i = {}

            novel_i[self.JSON_NOV_NAME]     = nov_info[self.JSON_NOV_NAME]
            novel_i[self.JSON_NOV_SLUG]     = nov_info[self.JSON_NOV_SLUG]
            novel_i[self.JSON_NOV_TAGS]     = nov_info[self.JSON_NOV_TAGS]
            novel_i[self.JSON_NOV_CHAP_CNT] = nov_info[self.JSON_NOV_CHAP_CNT]
            novel_i[self.JSON_NOV_GENRES]   = nov_info[self.JSON_NOV_GENRES]
            novel_i[self.JSON_NOV_ABBR]     = nov_info[self.JSON_NOV_ABBR]
            novel_i[self.JSON_NOV_SUMM]     = self._get_paragraphs(nov_info[self.JSON_NOV_SUMM])

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

        # TODO: Apply a strict filter to prevent things other than chapters from coming up

        paras = []
        bs_obj = BeautifulSoup(html_file, self.DEFAULT_HTML_PARSER)
        paras_tags = bs_obj.find_all('p')  # A list of BeautifulSoup Tag objects

        # Convert all the paragraphs to text and append to the list of paragraphs
        for ptag in paras_tags:
            paras.append(ptag.get_text().strip())

        return paras

    def _get_next_prev_urls(self, html_file):
        """
        Extract the URLs to next and previous chapters from the current HTML file
        """
        next_url = None
        prev_url = None

        # TODO: Parse the given HTML to extract links for next and previous chapter

        return next_url, prev_url
