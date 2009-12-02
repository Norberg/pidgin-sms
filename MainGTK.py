#!/usr/bin/env python
import sys
try:
 	import pygtk
  	pygtk.require("2.0")
except:
  	pass
try:
	import gtk
  	import gtk.glade
	import gobject
except:
	sys.exit(1)
import setting

class MainGTK:

	def __init__(self):	
		#Set the Glade file
		self.gladefile = "gui.glade" 
	        self.wTree = gtk.glade.XML(self.gladefile, "winMain") 
		self.wTree.signal_autoconnect(self)
		self.widget = self.wTree.get_widget
		self.readSettings()

	def readSettings(self):
		s = setting.readSettings()
		self.widget("txtMessage").set_text(s[0])
		self.widget("sbTimeout").set_text(s[1])
		self.widget("txtUserId").set_text(s[2])
		self.widget("txtPass").set_text(s[3])
		self.widget("txtReplayNr").set_text(s[4])

	def writeSettings(self):
		message = self.widget("txtMessage").get_text()
		timeout = self.widget("sbTimeout").get_text()
		userId = self.widget("txtUserId").get_text()
		passwd = self.widget("txtPass").get_text()
		replayNr = self.widget("txtReplayNr").get_text()
		setting.writeSettings(message,timeout,userId,passwd,replayNr)

	def on_btnSave_clicked(self, widget):
		self.writeSettings()
		self.widget("winMain").destroy()
