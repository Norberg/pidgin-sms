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

class MainGTK:

	def __init__(self):	
		#Set the Glade file
		self.gladefile = "gui.glade" 
	        self.wTree = gtk.glade.XML(self.gladefile, "winMain") 
		self.wTree.signal_autoconnect(self)
		self.widget = self.wTree.get_widget
	def on_winMain_destroy(self, widget):
		gtk.main_quit()
	def on_btnSave_clicked(self, widget):
		print "Saved.."
