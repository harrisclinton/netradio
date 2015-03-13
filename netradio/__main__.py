#!/usr/bin/env python

from netradio import *

if __name__ == '__main__':
	
	radio = NetRadio()

	#Start sound playback
	radio.play()

	#Start GUI/event polling
	radio.main()
