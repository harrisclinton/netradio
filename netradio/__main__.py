#!/usr/bin/env python

from netradio import *

if __name__ == '__main__':
	
	radio = NetRadio()
	
	#Some example stations. URI must be actual stream, not playlist/m3u etc.
	radio.add_station("WGBH Radio Boston Classical", "http://audio.wgbh.org:8004",None,None)
	radio.add_station("European Chillout", "http://mp3channels.webradio.antenne.de/chillout",None,None)

	#Start sound playback
	radio.play()

	#Start GUI/event polling
	radio.main()
