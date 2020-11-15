# read.py -- Read a chapter of some specified novel

import shell.cmdbase
import crawlers.cfactory as cfactory
from crawlers.cutils import chap_utils as cu
'''
follwing are the imports from prompt toolkit:

Application : for main full screen application to render
KeyBinding  : for key controls
Buffer and BufferControl,Document : To render the content on the screen
Window, HSplit, layout : For layout of the screen

'''

from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.containers import Window, HSplit, WindowAlign
from prompt_toolkit.widgets import Box, MenuContainer, FormattedTextToolbar
from prompt_toolkit.layout.layout import Layout


class ReadCommand(shell.cmdbase.CommandBase):
    """
    Opens a Reader for a given Chapter of given novel
    """
    DESCRIPTION = 'Reads the given Chapter'
    RELOAD_MESG = '\nPress Control-r to load the latest valid chapter.\n' + \
        '(OR), Press Control-t to load the first chapter you started with.\n'
    PARSING_ERR_MSG = "Error in Parsing Arguments"

    def __init__(self):
        super().__init__()
        # Adds argument for novel name [--novel/ -n]
        self.arg_parser.add_argument(
            '-n', '--novel', nargs='+', type=str, help='Name of the Novel')
        # Adds argument for chapter number [--chapter/ -c]
        self.arg_parser.add_argument(
            '-c', '--chapter', type=str, help='Chapter Number')
        self.starting_chap = 1
        self.novel = None                # will store the current novel name
        self.curr_chap_num = 1           # store current chapter number
        self.prev_chap = None            # store previous chapter object
        self.next_chap = None            # store next chapter object
        self.chapter = None              # store current chapter object
        self.chapter_content = ""        # current chapters content
        self.web_crawler = None          # crawler for current novel
        self.prev_chap_crawler = None    # store previous chapter number
        self.next_chap_crawler = None    # store next chapter number
        '''
        follwing are required to get initialized 
        for the full screen application to render
        '''
        # initalize the key binding object
        self.key_binding = KeyBindings()
        self.buffer = Buffer(document=Document(
            self.chapter_content, 0), read_only=True)
        # initialize buffer control which shows main content
        self.buf_control = BufferControl(
            buffer=self.buffer, key_bindings=self.key_binding)
        # initialize bottom menu content
        self.menu_content = " "*60 + \
                            "[Menu Controls]\nCtrl-Q : Back, Ctrl-N : Next Chapter, Ctrl-P : Previous Chapter," +\
                            " Ctrl-r : Load Last Valid Chapter, Ctrl-t : Load with Starting Chapter"
        self.menu = FormattedTextToolbar(
            text=self.menu_content)
        # initialize top menu object
        self.top_menu = Window(content=FormattedTextControl(
            text="Chapter : " + str(self.curr_chap_num)), height=1)

        # forms windows layout containing topmenu , buffer control and bottom menu
        # self.content = HSplit([
        #     self.top_menu,
        #     Window(content=self.buf_control, wrap_lines=True),
        #     self.menu
        # ], padding_char='-', padding=1, padding_style='#ffff00')
        self.content = HSplit([
            Box(self.top_menu, padding_bottom=2,
                style='#eceff1 bg:#6002ee'),
            Box(Window(content=self.buf_control, wrap_lines=True, style='#eceff1 bg:#263238'),
                padding_left=1, padding_right=1, style='#eceff1 bg:#263238'),
            Box(self.menu, padding_top=1, style='#eceff1 bg:#2001ee')
        ])
        self.container = self.content
        self.layout = Layout(self.container)

    def _next_chapter(self):
        # get the next chapter result and crawler
        status, result, newcrawler = self.web_crawler.next_chapter()
        # if status = 0 we got valid next chapter
        if status == 0:
            # update current chapter object
            self.chapter = result
            # update current chapter number
            self.curr_chap_num = result[cu.GET_CHAP_TITLE_KEY]
            # update curreent chapter content
            self.chapter_content = '\n\n'.join(
                self.chapter[cu.GET_CHAP_CONTENTS_KEY])
            # update the web crawler
            self.web_crawler = newcrawler
        # TODO : what if error happens here ?
        else:
            # just the load the error message into chapter content
            self.chapter_content = result + self.RELOAD_MESG
        return status

    def _prev_chapter(self):
        # get the next chapter result and crawler
        status, result, newcrawler = self.web_crawler.previous_chapter()
        # if status = 0 we got valid prev chapter
        if status == 0:
            # update current chapter object
            self.chapter = result
            # update current chapter number
            self.curr_chap_num = result[cu.GET_CHAP_TITLE_KEY]
            # update curreent chapter content
            self.chapter_content = '\n\n'.join(
                self.chapter[cu.GET_CHAP_CONTENTS_KEY])
            # update the web crawler
            self.web_crawler = newcrawler
        # TODO : what if error happens here ?
        else:
            self.chapter_content = result + self.RELOAD_MESG
        return status

    def key_init(self):
        @self.key_binding.add('c-q')
        def exit_(event):
            event.app.exit()

        @self.key_binding.add('c-r')
        def reload_(event):
            # reload the chapter content to last valid content
            self.chapter_content = '\n\n'.join(
                self.chapter[cu.GET_CHAP_CONTENTS_KEY])
            self.changebuffercontent()

        @self.key_binding.add('c-t')
        def startreload_(event):
            self.curr_chap_num = self.starting_chap
            self.read_current_chapter()
            self.changebuffercontent()
            self.updateTopMenu()

        @self.key_binding.add('c-n')
        def next_(event):
            if self.next_chap is None:
                status = self._next_chapter()
                if status == 0:
                    self.next_chap = None
            self.changebuffercontent()
            self.updateTopMenu()

        @self.key_binding.add('c-p')
        def prev_(event):
            self._prev_chapter()
            self.updateTopMenu()
            self.changebuffercontent()

    def read_current_chapter(self):
        status, result = self.web_crawler.get_chapter(self.curr_chap_num)
        if status != 0:
            return status, result
        self.novel = result[cu.GET_CHAP_NOV_NAME_KEY]
        self.chapter = result
        self.curr_chap_num = result[cu.GET_CHAP_TITLE_KEY]
        self.chapter_content = '\n\n'.join(
            self.chapter[cu.GET_CHAP_CONTENTS_KEY])
        return 0, result

    def updateTopMenu(self):
        self.top_menu.content.text = "Novel : " + str(self.novel) + \
            " Chapter: " + \
            str(self.curr_chap_num)

    def changebuffercontent(self):
        self.buffer.set_document(
            Document(self.chapter_content, 0), bypass_readonly=True)

    def run(self):
        self.application = Application(
            layout=self.layout, key_bindings=self.key_binding, full_screen=True)
        self.application.run()

    def help(self):
        return self.__doc__

    def execute(self, cmd_args):
        '''
        initalizes reader and opens a full screen application for reading
        '''
        args = self._parse_args(cmd_args)
        if args is None:
            return -1, self.PARSING_ERR_MSG

        print(self.novel, self.curr_chap_num)
        crawler = cfactory.CrawlerFactory()
        self.web_crawler = crawler.get_crawler(self.novel)
        self.key_init()
        status, res = self.read_current_chapter()
        if status == 0:
            self.changebuffercontent()
            self.updateTopMenu()
            self.run()
            return 1, None
        else:
            return -1, res

    def _parse_args(self, cmd_args):
        '''
        Parses the user argument and store them in novel and curr chapter 
        '''
        try:
            args = self.arg_parser.parse_args(cmd_args)
            self.novel = ' '.join(args.novel)
            if args.chapter is not None:
                self.starting_chap = args.chapter
                self.curr_chap_num = args.chapter

        except:
            return None
        return args

    def _parse_result(self, result):
        pass
