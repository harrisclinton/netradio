import pygame, os, sys
from looper import *

"""
PgGui is a very simple GUI toolkit built on Pygame.
It is designed to allow coding simple 2D graphical GUIs in Pygame,
such as for simple games or other apps running on a Raspberry Pi.

It handles pygame blitting, screen updates, and event handling transparently.

Version 0.1.0, 2015.3.13
Chris Harrington
chris.harrington.jp@gmail.com

See netradio.py for example usage.
https://github.com/harrisclinton/netradio

"""

class PgContext(object):
    
    def __init__(self, fps, w, h, caption):

        self.path = None
        
        pygame.init()

        self.clock = pygame.time.Clock()        
        self.fps = fps
        self.width = w
        self.height = h
        
        self.events = {} #dict of events to watch for and associated widgets
        
        self.keys = {} #list of keys to watch out for
        
        self.widgets = [] #list of widgets
        
        self.surface = None
        
        self.background = None
        
        pygame.display.set_caption(caption)

    def add_widget(self, widget):
        self.widgets.append(widget)
        widget.context = self
        for event_handler in widget.events:
            self.__events_append(event_handler)
            
    def add_event(self, event_handler):
        self.__events_append(event_handler)

    def __events_append(self, event_handler):
        if event_handler.event in self.events:
            self.events[event_handler.event].append(event_handler.handler)
        else:
            self.events[event_handler.event] = [event_handler.handler]
        if event_handler.key:
            if event_handler.key in self.keys:
                self.keys[event_handler.key].append(event_handler.handler)
            else:
                self.keys[event_handler.key] = [event_handler.handler]
        
    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type in self.events:
                    if event.type == pygame.KEYDOWN:
                        if event.key in self.keys:
                            for handler in self.keys[event.key]:
                                handler(event.key)
                    else:
                        for handler in self.events[event.type]:
                            handler()
            self.draw_update()
                                                
    def draw_all(self):
        self.surface.blit(self.background, (0,0))
        for widget in self.widgets:
            widget.draw()
            self.surface.blit(widget.surface, (widget.x, widget.y))
        pygame.display.flip()

    def draw_update(self):
        for widget in self.widgets:
            if widget.update:
                widget.draw()
                self.surface.blit(widget.surface, (widget.x, widget.y))
                widget.update = False
        pygame.display.flip()        
        #self.clock.tick(self.fps)
        
    def quit(self):
        pygame.quit()
        sys.exit()	        

class PgEventHandler():
    
    def __init__(self, handler, event, key, args):
        self.handler = handler
        self.event = event
        self.key = key
        self.args = args
        if key:
            self.key = key

class PgWidget(object):
    #Base widget class
    #More shared behavior will be added from other child widgets
    #as more of those are created
    
    def __init__(self):
        self.update = False
        
        self.surface = None
        self.background = None
        self.foreground = None
        self.layers = []
        self.context = None
                
    def draw(self):
        for layer in self.layers:
            if layer:
                self.surface.blit(layer, (0,0))
        

class PgRoller(PgWidget):
    
    """
    A Pygame Roller implements a widget representing a horizontal rolling cylinder behind a frame
    This allows a scrolling list of text entries to be scrolled through up and down
    """
    
    def __init__(self, items, background, foreground, font, fontsize, color, x, y, keyup, keydown):
        
        PgWidget.__init__(self)
        
        self.items = items                                      #dict of string keys and associated objects
        self.looper = Looper(0, len(self.items), 0)             #looping interator object
        self.texts = []                                         #Array of font.render() surfaces
        self.background = pygame.image.load(background)         #Background layer image surface
        self.foreground = pygame.image.load(foreground)         #Foreground layer image surface
        self.width = self.background.get_width()                #Widget width
        self.height = self.background.get_height()              #Widget height
        self.center = (self.height / 2) - 1                     #Vertical center line on widget
        self.surface = pygame.Surface((self.width,self.height), pygame.SRCALPHA, 32)    #Widget base surface
        
        self.x = x                                              #Widget x position on parent
        self.y = y                                              #Widget right position on parent
        self.font = pygame.font.Font(font, fontsize)            #Widget font
        self.color = color                                      #Widget font color
        self.spacing = self.font.get_linesize()                 #Widget font line spacing
        self.scroll_pos = self.center                           #Offset of text y position for scroll animation
        self.on_scroll = None                                   #Holds external function to trigger when scrolling up or down
        self.scrollspeed = 1                                    #Number of pixels to scroll each update

        #Create the list of text surfaces
        for key in self.items:
            textsurf = PgTextSurf(self.font, key.name, self.color)
            textsurf.x_off = (self.width - textsurf.surf.get_width()) / 2
            self.texts.append(textsurf)
            textsurf.index = len(self.texts) - 1
            
        #Register events to respond to and associated handlers
        self.events = []
        self.events.append(PgEventHandler(self.roll_up, pygame.KEYDOWN, pygame.K_UP, None))
        self.events.append(PgEventHandler(self.roll_down, pygame.KEYDOWN, pygame.K_DOWN, None))
        
        #Populate layers list for drawing
        self.layers.append(self.background)
        self.layers.append(None)            #Blank layer for the text layer
        self.layers.append(self.foreground)
        
        
    def draw(self):

        textlayer = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)        
        if len(self.items) > 1:
            #If there are 2 or more stations registered
            #Expand list before/after to allow scrolling text
            
            increment = -2
            while increment < 3:
                text = self.texts[self.looper.get_offset(increment)]
                text.rect.topleft = (text.x_off, self.scroll_pos + (increment * self.spacing * 1.35) - text.y_off)
                textlayer.blit(text.surf, text.rect)
                increment += 1
            
        else:
            text = self.texts[0]
            text.rect.topleft = (text.x_off, self.scroll_pos - text.y_off )
            textlayer.blit(text, text.rect)
                        
        self.layers[1] = textlayer
        super(PgRoller, self).draw()
        
    def roll_up(self, key):
        self.animate_scroll(-1)
        self.on_update(self.texts[0].index)
        
    def roll_down(self, key):
        self.animate_scroll(1)
        self.on_update(self.texts[0].index)                
        
    #Animate the station roll
    def animate_scroll(self, direction):
        startpos = self.scroll_pos
        if len(self.texts) > 1:
            if direction > 0:
                while self.scroll_pos > startpos - (self.spacing * 1.35):
                    self.update = True
                    self.scroll_pos -= direction * self.scrollspeed
                    self.context.draw_update()
                self.scroll_pos = self.center
                text = self.texts.pop(0)
                self.texts.append(text)
                self.update = True
                self.context.draw_update()

            else:
                while self.scroll_pos < startpos + (self.spacing * 1.35):
                    self.update = True
                    self.scroll_pos -= direction * self.scrollspeed
                    self.context.draw_update()
                self.scroll_pos = self.center
                text = self.texts.pop()
                self.texts.insert(0, text)
                self.update = True
                self.context.draw_update()


class PgTextSurf():
    
    def __init__(self, font, string, color):
        self.string = string
        self.surf = font.render(string, True, color)
        self.rect = self.surf.get_rect()
        self.w = self.rect.width
        self.h = self.rect.height
        #self.center = self.get_ascent() / 2
        self.x_off = 0
        self.y_off = font.get_ascent() / 2