"""

PyGame GUI for a Raspberry Pi based Net Radio device

Version: 0.2.0, 2015.3.7

chris.harrington.jp@gmail.com

Change the radio station using the up/down arrow keys on keyboard
Quit by pressing ESC

Stations must be added/edited manually in __main__

Things to do:
	Further optimise screen refresh for Raspberry Pi - possibly use PyOpenGL
		Done:Splice gui graphics more to avoid full screen blit
 	Further abstraction
		Done:Separate "player" class to allow easy swap of sound library
		Separate class for all visuals to allow replacing GUI modules used
		i.e. optionally replace PyGame with some other library
	Parsing of playlist files to extract station name/url (.m3u, .pls, .xspf etc.)
	Web interface for headless operation
		Control from PC/phone/tablet browser
	Add GUI widgets in empty space on screen such as
		Audio level meter - functionality available in Gstreamer 1.0
		Stream bitrate meter
	Interface to add/edit/remove stations
	Interface to select line in (such as iPod) for playback on speakers
	Interface to play local files instead of streams
	Socket to receive playlist files for auto registration (i.e. send from phone etc.)
	Possibly get a Shoutcast directory API key to add an interface
	for searching for streams
	Implement skinning to allow replacing the GUI without editing code.

"""

import pygame, sys, platform, os
from gi.repository import GObject, Gst
from station import *
from rgbcolors import *
from player import *
		
class NetRadio():
	
	def __init__(self):
		
		self.path = self.get_exec_path()
		
		self.is_raspi = False #Flag true when run on Arm v6l machine
		
		if platform.machine() == 'armv6l':
			self.is_raspi = True
			
		self.stations = []	#List of streaming station objects
		self.selected = 0	#Index of current selected station
		
		self.colors = RgbColors()	#ENUM of colors
		
		self.scroll_step = 1	 #No. pixels to scroll each step

		self.screen_offset = [0,0] #Offset for GUI graphics
		self.text_offset = [0,38] #Offset for text, Y depends on font
		
		pygame.init()
		self.clock = pygame.time.Clock()
		self.fps = 10
		
		#Various possible settings for the screen
		
		#GUI Graphics currently too wide
		if self.is_raspi:
			#Raspberry Pi 480 x 360 PiTFT 3.5" screen
			self.surface = pygame.display.set_mode((570,360), pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN)
			self.scroll_step = 5
		else:
			#Default on PC
			self.surface = pygame.display.set_mode((570,360), pygame.DOUBLEBUF)
			
		pygame.display.set_caption('Radio')
		
		#Need to contact font designers to make sure it is distributable
		#Y Offset depends on font. Could probably calculated it
		#based on text surface rectangle

		#http://www.dafont.com/linowrite.font
		self.font = pygame.font.Font(self.path + "/gui/linowrite.ttf", 32)
		#self.text_offset[1] = 58

		#Alternative font
		#http://www.dafont.com/afl-font-pespaye-no.font
		#self.font = pygame.font.Font(self.path + "/gui/aflfont.TTF", 32)
		#self.text_offset[1] = 48
	
		self.radioback = pygame.image.load(self.path + '/gui/RadioBack.png')
		self.radiopaper = pygame.image.load(self.path + '/gui/RadioPaper.png')
		self.radioface = pygame.image.load(self.path + '/gui/RadioOverlay.png')
		self.surface.blit(self.radioback, self.screen_offset)
		
		self.player = Player(self.is_raspi)
	
	#Need to break event handler loop out to separate 
	#function for cleanliness	
	def main(self):
		while True:
			for event in pygame.event.get(): # event handling loop
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_DOWN:
						#Going up!
						self.increment_scroll(-1)
					if event.key == pygame.K_UP:
						#Going down!
						self.increment_scroll(1)
					if event.key == pygame.K_ESCAPE:
						self.quit()
				if event.type == pygame.QUIT:
					self.quit()
											
			self.updateScreen(self.text_offset[1])
			self.clock.tick(self.fps)
			print self.player.level_l, self.player.level_r
		
	def add_station(self, station_name, station_uri, user, password):
		if self.verify_station(station_uri):
			self.stations.append(Station(station_name, station_uri, user, password))

	def verify_station(self, uri):
		#Add error checking on stream uri
		return True
			
	def play(self):
		self.player.play(self.stations[self.selected].uri)
		
	def stop(self):
		self.player.stop()
		
	#Increment or decrement the station selection
	def increment_scroll(self, direction):
		self.animate_scroll(direction)
		self.selected -= direction
		if self.selected == len(self.stations):
			self.selected = 0
		if self.selected < 0:
			self.selected = len(self.stations) - 1
		self.play()		
		
	#Animate the station roll
	def animate_scroll(self, direction):
	
		ypos = self.text_offset[1]
		if len(self.stations) > 1:
			if direction > 0:
				while ypos < 106:
					ypos += direction * self.scroll_step
					self.updateScreen(ypos)
			else:
				while ypos > 10:
					ypos += direction * self.scroll_step
					self.updateScreen(ypos)
		else:
			pass

	#Refresh the pygame display
	def updateScreen(self, ypos):
	
		textmaster = pygame.Surface((365,100), pygame.SRCALPHA, 32)
	
		if len(self.stations) > 1:
			#If there are 2 or more stations registered
			#Expand list before/after to allow scrolling text
			locstat = self.stations * 3
			pos = len(self.stations) + self.selected
		
			#Define station text to display: 3 visible, 2 hidden
			#Need to refactor x position calcuation
			#I am bad at math
			textsurf0 = self.font.render(locstat[pos-2].name, True, self.colors.black)
			textrect0 = textsurf0.get_rect()
			textrect0.topleft = (self.text_offset[0] + ((365 - textsurf0.get_width()) / 2), ypos-96)
		
			textsurf1 = self.font.render(locstat[pos-1].name, True, self.colors.black)
			textrect1 = textsurf1.get_rect()
			textrect1.topleft = (self.text_offset[0] + ((365 - textsurf1.get_width()) / 2), ypos-48)
		
			textsurf2 = self.font.render(locstat[pos].name, True, self.colors.black)
			textrect2 = textsurf2.get_rect()
			textrect2.topleft = (self.text_offset[0] + ((365 - textsurf2.get_width()) / 2), ypos)
		
			textsurf3 = self.font.render(locstat[pos+1].name, True, self.colors.black)
			textrect3 = textsurf3.get_rect()
			textrect3.topleft = (self.text_offset[0] + ((365 - textsurf3.get_width()) / 2), ypos+48)
		
			textsurf4 = self.font.render(locstat[pos+2].name, True, self.colors.black)
			textrect4 = textsurf4.get_rect()
			textrect4.topleft = (self.text_offset[0] + ((365 - textsurf4.get_width()) / 2), ypos+96)
		
			textmaster.blit(textsurf0, textrect0)
			textmaster.blit(textsurf1, textrect1)
			textmaster.blit(textsurf2, textrect2)
			textmaster.blit(textsurf3, textrect3)
			textmaster.blit(textsurf4, textrect4)
		else:
			#If there is only one station registered
			textsurf = self.font.render(self.stations[0].name, False, BLACK)
			textrect = textsurf.get_rect()
			textrect.topleft = (self.text_offset[0] + ((365 - textsurf.get_width()) / 2), ypos)
			textmaster.blit(textsurf, textrect)

		#Draw the composite result
		#Only redraws necessary area
		self.surface.blit(self.radiopaper, (99,20))
		self.surface.blit(textmaster, (99,20))
		self.surface.blit(self.radioface, (99,20))
	
		#pygame.display.update()
		pygame.display.flip()

	def get_exec_path(self):
		try:
			sFile = os.path.abspath(sys.modules['netradio'].__file__)
		except:
			sFile = sys.executable
		return os.path.dirname(sFile)
		
	def quit(self):
		self.player.stop()
		pygame.quit()
		sys.exit()		
