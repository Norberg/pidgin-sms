def writeSettings(*settings):
	f = file("settings.dat", "w")
	for setting in settings:
		f.write(str(setting) + "\n")
	f.close()
def readSettings():
	f = file("settings.dat", "r")
	tmp = f.readlines()
	result = []
	for line in tmp:
		try:
			result.append(int(line.strip("\n")))
		except ValueError: #isnt an integer.
			result.append(line.strip("\n"))
	return result
