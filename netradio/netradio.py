import pygame, sys, platform, os
from radio import *
from pggui import *

"""
GUI for a Raspberry Pi based Net Radio device
Actual GUI library is kept separate
This version uses Pygame as the GUI.

Version: 0.3.0, 2015.3.13

chris.harrington.jp@gmail.com

Change the radio station using the up/down arrow keys on keyboard
Quit by pressing ESC

Stations must be added/edited manually in __main__

Things to do:
    Further optimise screen refresh for Raspberry Pi - possibly use PyOpenGL
        Done:Splice gui graphics more to avoid full screen blit
    Further abstraction
        Done:Separate "player" class to allow easy swap of sound library
        Done: Separate class for all visuals to allow replacing GUI modules used
        i.e. optionally replace PyGame with some other library like Pyglet
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

class NetRadio(Radio, PgContext):
    
    def __init__(self):

        Radio.__init__(self)
        PgContext.__init__(self, 10, 570, 360, "NetRadio")

        self.path = self.get_exec_path()
        
        self.is_raspi = False #Flag true when run on Arm v6l machine
        
        if platform.machine() == 'armv6l':
            self.is_raspi = True
        
        if self.is_raspi:
            #Raspberry Pi 480 x 360 PiTFT 3.5" screen
            self.surface = pygame.display.set_mode((self.width,self.height), pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN)
            #self.scroll_step = 5
        else:
            #Default on PC
            self.surface = pygame.display.set_mode((self.width,self.height), pygame.DOUBLEBUF)

        self.add_event(PgEventHandler(self.quit, pygame.KEYDOWN, pygame.K_ESCAPE, None))
        
        self.load_skin()

        self.draw_all()

        #self.main()
    
    def load_skin(self):
        #This function will load external config and skin in the future
        #Settings hard coded for now

        #Assume that .config contains list of radio stations
        self.add_station("WCRB Radio Boston Classical", "http://audio.wgbh.org:8004",None,None)
        self.add_station("European Chillout", "http://mp3channels.webradio.antenne.de/chillout",None,None)
        self.add_station("Cool Fahrenheit", "http://86.127.178.103:8000", None, None)
        self.add_station("Venice Classic Radio Italia", "http://109.123.116.202:8020/stream", None, None)
        self.add_station("Groove Salad", "http://173.239.76.148:8032", None, None)

        #Assume that .skin contains the following graphics/widget definitions
        #Background image
        self.background = pygame.image.load(self.path + '/gui/RadioBack.png')
        #Radio station roller widget
        roller = PgRoller(self.stations, self.path + '/gui/RadioPaper.png', self.path + '/gui/RadioOverlay.png', self.path + '/gui/linowrite.ttf', 32, (0,0,0), 99, 20, pygame.K_UP, pygame.K_DOWN)
        #Set on_update handler for roller widget - called when widget rolls up or down
        roller.on_update = self.change_station
        if self.is_raspi:
            roller.scrollspeed = 3
        #Register the widget with the pygame context object
        self.add_widget(roller)
        
        # To add: left and right stereo level widgets, maybe, depending on resulting frame rate
        
    #Change the playing radio station when roller widget changes
    def change_station(self, station):
        self.selected = station
        self.play()

    #Determine runtime directory for loading assets        
    def get_exec_path(self):
        try:
            sFile = os.path.abspath(sys.modules['netradio'].__file__)
        except:
            sFile = sys.executable
        return os.path.dirname(sFile)

    #Quit. Perform any necessary cleanup before calling quit in the pygame context object
    def quit(self, key):
        self.stop()
        super(NetRadio, self).quit()
        




