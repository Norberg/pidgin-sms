# Copyright 2009 Simon Norberg
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
		result.append(line.strip("\n"))
	return result
