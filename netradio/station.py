class Station():
	def __init__(self, station_name, station_uri, user, password):
		if len(station_name) > 19:
			station_name = station_name[0:18] + "..."
		self.name = station_name
		self.uri = station_uri
		#Not yet used, for streaming services requiring login
		self.user = user
		self.password = password
