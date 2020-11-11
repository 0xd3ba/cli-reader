from __future__ import unicode_literals
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import VSplit, Window,HSplit,FloatContainer,Float
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
# from prompt_toolkit.layout.dimension import Dimension
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document

	
class reader(object):
	def __init__(self):
		self.curr_chap_num=1
		self.prev_chap_num=0
		self.next_chap_num=2
		self.prev_chap=""
		self.next_chap=""
		self.doc = ""
		self.key_binding = KeyBindings()
		self.buffer = Buffer(document=Document(self.doc, 0),read_only=True)
		self.buf_control = BufferControl(buffer=self.buffer,key_bindings=self.key_binding)
		self.menu_content = " "*70 + "[Menu Controls]\nCtrl-Q : Back Ctrl-N:Next Chapter Ctrl-P:Previous Chapter"
		self.menu = Window(content=FormattedTextControl(text=self.menu_content),height=2)
		self.top_menu = Window(content=FormattedTextControl(text="Chapter : " + str(self.curr_chap_num) ),height=1)

		self.content = HSplit([
				self.top_menu,
                Window(content=self.buf_control,wrap_lines=True),
                self.menu
            ],padding_char='-',padding=1,padding_style='#ffff00')
		self.container = self.content
		self.layout = Layout(self.container)
		#self.container = FloatContainer(
         #   content=self.content,
          #  floats=[
           #     Float(xcursor=True, ycursor=True,
            #          content=self.menu,height=2,bottom=0,),
            #]
    	#)



	def updateChapterNumber(self):
		self.top_menu.content.text = "Chapter : "+ str(self.curr_chap_num)

	def next_chapter(self,chap_num):
		self.next_chap = "Xia Qingyue appeared between the arms of two bridesmaids. She wore a red phoenix coronet on top of her head."
	
	def prev_chapter(self,chap_num):
		self.prev_chap = "Xiao Lingxi cried out and sprang backwards like a frightened rabbit. Her fingers touched her numb lips as her beautiful eyes widened in surprise"

	def key_init(self):
		@self.key_binding.add('c-q')
		def exit_(event):
			event.app.exit()

		@self.key_binding.add('c-n')
		def next_(event):
			if self.next_chap == "":
				self.next_chapter(self.next_chap_num)
			self.prev_chap_num = self.curr_chap_num
			self.curr_chap_num = self.next_chap_num
			self.next_chap_num = self.curr_chap_num + 1
			self.prev_chap = self.doc
			self.doc = self.next_chap
			self.next_chap=""
			self.changebuffercontent()
			self.updateChapterNumber()
			
		@self.key_binding.add('c-p')
		def prev_(event):
			if self.curr_chap_num == 1:
				return
			if self.prev_chap == "":
				self.prev_chapter(self.prev_chap_num)
			self.next_chap_num = self.curr_chap_num
			self.curr_chap_num = self.prev_chap_num
			self.prev_chap_num = self.curr_chap_num -1
			self.next_chap = self.doc
			self.doc = self.prev_chap
			self.prev_chap = ""
			self.updateChapterNumber()
			self.changebuffercontent()

	def changebuffercontent(self):
		self.buffer.set_document(Document(self.doc,0),bypass_readonly=True)
	def run(self):
		self.application = Application(layout =self.layout,key_bindings=self.key_binding,full_screen=True)
		self.application.run()



initial_conent = """Floating Cloud City was the smallest city of the Blue Wind Empire. It was so small that it wasn't even suitable to be called a city; perhaps calling it a town would be more appropriate. Floating Cloud City was not only the smallest city but was also the most geographically remote in terms of location. The population, economy, and even the average profound strength was the lowest of the low. These days, Floating Cloud City’s residents often mock themselves for being a forgotten corner in the Blue Wind Empire.

Floating Cloud City was particularly lively today for it was Xiao Che and Xia Qingyue’s big wedding day. Nobody would care if it was only Xiao Che’s wedding but Xia Qingyue’s marriage was Floating Cloud City’s biggest sensational event.

The Xia Clan was not a clan that solely trained in the arts of the profound. It was a clan that specialized in business for generations. Although they could not be said to be wealthy among others of the Blue Wind Empire; on Floating Cloud City’s list of the most prosperous clans, Xia Clan was at the top. However, this did not mean that the Xia Clan was weak. With their abundant wealth, they could naturally afford to hire experts to protect their vast fortune. The leader of the Xia Clan had two children: Xia Yuanba and Xia Qingyue. Both his son and daughter had no interest in the family business. They solely focused on training in the ways of the profound. Xia Hongyi had never opposed their decision and instead allowed them to continue their path. After Xia Qingyue surprised Floating Cloud City with her talent, it was even more unlikely that he would prevent her growth. Due to Xia Qingyue’s amazing god-given gift, Floating Cloud City’s major families were on their best behavior in their presence…. After all, it was widely acknowledged that Xia Qingyue may reach the Earth Profound Realm or even the Sky Profound Realm someday in the future. At that point, the Xia Clan would not only have the most wealth, but would also be the most dominating force in Floating Cloud City.

However, that Xia Clan had let the city’s most brilliant girl marry Xiao Che, a good-for-nothing with no possible future. Who knows how many people regret that decision…. Of course, there were more people with feelings of envy and jealous hate."""

if __name__ == '__main__':
	r = reader()
	r.key_init()
	#initial_conent = "Floating Cloud City was the smallest city of the Blue Wind Empire. It was so small that it wasn't even suitable to be called a city; perhaps calling it a town would be more appropriate. Floating Cloud City was not only the smallest city but was also the most geographically remote in terms of location. The population, economy, and even the average profound strength was the lowest of the low. These days, Floating Cloud City’s residents often mock themselves for being a forgotten corner in the Blue Wind Empire."
	r.doc = initial_conent
	r.changebuffercontent()
	r.run()