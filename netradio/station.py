"""
A simple class definition of a online streaming radio station object

Version 0.1.0, 2015.3.7
chris.harrington.jp@gmail.com

"""

class Station():
	def __init__(self, station_name, station_uri, user, password):
		if len(station_name) > 19:
			station_name = station_name[0:18] + "..."
		self.name = station_name
		self.uri = station_uri
		#Not yet used, for streaming services requiring login
		self.user = user
		self.password = password
