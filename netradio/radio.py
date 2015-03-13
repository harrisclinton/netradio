"""

radio.py
Version: 0.1.0, 2015.3.13
chris.harrington.jp@gmail.com

Radio class is a simple wrapper class for the
Player class in player.py which is kept separate so that
the radio class does not directly reference any media libraries
such as Gst etc.

It adds "radio station" handling functions and other similar functions
to be called by the NetRadio gui class.

Things to do:
	Parsing of playlist files to extract station name/url (.m3u, .pls, .xspf etc.)

"""

import sys, platform, os
from station import *
from player import *
		
class Radio(object):
	
	def __init__(self):
		
		#self.__path = self.get_exec_path()
					
		self.stations = []	#List of streaming station objects
		self.selected = 0	#Index of current selected station		
		
		self.player = Player()
	
	#Need to break event handler loop out to separate 
	#function for cleanliness	

		
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
		


