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
import MainGTK

class StartGTK:

	def __init__(self):	
		#Set the Glade file
		self.gladefile = "gui.glade" 
	        self.wTree = gtk.glade.XML(self.gladefile, "winStart") 
		self.wTree.signal_autoconnect(self)
		self.widget = self.wTree.get_widget

	def on_winStart_destroy(self, widget):
		gtk.main_quit()

	def on_btnExit_clicked(self, widget):	
		gtk.main_quit()

	def on_btnSettings_clicked(self, widget):
		MainGTK.MainGTK()	
