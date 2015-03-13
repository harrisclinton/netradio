from gi.repository import GObject, Gst, GLib
import threading, math, platform

"""
A audio player class for the Radio class to separate
player functions so that the Radio class itself
does not depend on a particular playback library

v. 0.1.1 2015.3.7
Chris Harrington
chris.harrington.jp@gmail.com

To Do:
*Process other messages besides level
*particularly to handle audio file playback better
*Possibly handle a neutral playlist format?

"""

class Player():
    
    def __init__(self):

        GObject.threads_init()
        Gst.init(None)

        is_arm = False #Flag true when run on Arm v6l machine
        
        if platform.machine() == 'armv6l':
            is_arm = True

        self.playbin = Gst.ElementFactory.make('playbin', None)
        
        #Properties to hold the current audio level (0 to 100)
        self.level_l = 0
        self.level_r = 0
        
        #Ensure ARM architecture uses Alsa sink
        #Gstreamer does not use default sound device on
        #Raspberry Pi unless specified for some reason
        #Otherwise, use autoaudiosync as the sink on PC etc.
        #In future: add functionality to check available devices??
        if is_arm:
            sink = Gst.ElementFactory.make('alsasink', None)
        else:
            sink = Gst.ElementFactory.make('autoaudiosink', None)

        #Create a "level" element to provide audio level data
        level = Gst.ElementFactory.make('level', None)

        #Create a bin as a dummy sink to contain the level and actual sink
        dummy_sink = Gst.Bin.new("dummysink")
        #Add the level and sink
        dummy_sink.add(level)
        dummy_sink.add(sink)
        #link them
        Gst.Element.link(level, sink)
        #Create a pad from the level element sink
        pad = Gst.Element.get_static_pad(level, "sink")
        #Create a ghost pad pointing to the pad
        ghost_pad = Gst.GhostPad.new("sink", pad)
        Gst.Pad.set_active(ghost_pad, True)
        #Add the ghost pad to the bin
        Gst.Element.add_pad(dummy_sink, ghost_pad)
        #Finally, assign the bin as the sink for the playbin 
        self.playbin.set_property('audio-sink', dummy_sink)
        
        #Now set up interrupt to get the level info
        bus = self.playbin.get_bus()
        
        bus.enable_sync_message_emission()    
        bus.connect('message', self.playbin_message)
        bus.add_signal_watch_full(GLib.PRIORITY_DEFAULT)
        print "initialize done"
        
        #And run a main loop thread for player
        #To get messages rolling
        g_loop = threading.Thread(target=GObject.MainLoop().run)
        g_loop.daemon = True
        g_loop.start()

    def play(self, uri):
        
        if self.validate_uri(uri):
            self.playbin.set_state(Gst.State.NULL)
            self.playbin.set_property('uri', uri)
            self.playbin.set_state(Gst.State.PLAYING)
            
    def playbin_message(self, bus, message):
        struct = message.get_structure()
        #print struct.get_name()
        #Peak DB values range from around -70 to 0.
        #Disgard everything below -50 and over 0 and convert to range 0 to 100)
        if struct.get_name() == 'level':
            self.level_l = min(max(0, (100 - int(round(struct.get_value('peak')[0] * -2)))),100)
            self.level_r = min(max(0, (100 - int(round(struct.get_value('peak')[1])) * -2)),100)

    def stop(self):
        
        self.playbin.set_state(Gst.State.NULL)
        
    def validate_uri(self, uri):
        
        if Gst.uri_is_valid(uri):
            uri_type = Gst.uri_get_protocol(uri)
            if uri_type == "file":
                if os.path.isfile(uri):
                    return True
                else:
                    return False
            else:
                #Network stream uri
                return True
        else:
            return False
            