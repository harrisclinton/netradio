A very simple retro-look net radio app in Python 2.7/PyGame/Gstreamer for the Raspberry Pi (and Desktop PC).

Version 0.1.0

This program is designed for use on a Raspberry Pi with any type of small screen and (preferably) USB audio device for building small Internet radio streaming player devices. The latest firmware and 3.18 kernel is required for smooth audio output. This is a limitation of the Raspberry Pi during streaming playback effecting all hardware at least up to the B+ due to Ethernet and USB using the same bus - playback on older kernels/firmware will feature audible pops at about six pops per second due to some kind of buffer underflow - the issue is fixed in the latest kernel/firmware. For details, see:
http://www.runeaudio.com/forum/my-solution-to-pops-and-clicks-t165.html

The GUI is designed to give a retro feel which can be modified by replacing the included graphic files.

The current version requires Python 2.7.x, GObject, Gstreamer 1.0, the python bindings thereof, and PyGame.

This has only been tested on Ubuntu Gnome 14.10 and Raspbian running the 3.18 kernel on a Rasberry Pi B+ with latest firmware as of 2015.3.6.

Development status is early alpha. Included functionality is to display a scrolling menu of pre-registered audio stream uris which are played automatically on launch and when selected. Selection uses the up and down arrow keys. The app can be closed by pressing Esc or clicking the window close window decoration (on PC only - full screen mode is used on the Raspberry Pi).

For now, you can add your own radio stations with NetRadio.add_station(station_name, station_uri). The URI must be the actual stream URI, not the URL of a playlist file (such as m3u).

This application is released under the GNU GPL v3.0 license or later (GPLv3+).

The following third party materials are used in the GUI (everything else hand drawn in GIMP):

Original source of the wood texture modified in GIMP for the GUI:
ResurgidaResources on DeviantArt
http://resurgidaresources.deviantart.com/art/Wood-texture-I-101021540
Restrictions: permission not required for use, but please attribute and link.
Please like his work if you have a DeviantArt account

Typewriter Font:
Linowrite by Lennard Glitter
(Free for personal use)
http://www.dafont.com/linowrite.font
This font is "free for personal use" and therefore third party distribution rights are unclear.
For that reason, the font is not included in this archive and must be downloaded by each user for their own personal use, or replaced with an alternative. Download the font from the above URL and place the .ttf file in the gui directory.
Optionally, use a different font. Place your font of choice in the gui directory and either rename it to linowrite.ttf or change the source to point to the new font.

GIMP files used to create the GUI can be found in the assets directory at https://github.com/harrisclinton/netradio.git

Roadmap:

	Further optimise screen refresh for Raspberry Pi - possibly use PyOpenGL
		Done:Splice gui graphics more to avoid full screen blit
 	Further abstraction
		Separate "player" class to allow easy swap of sound library
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

