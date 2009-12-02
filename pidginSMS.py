#!/usr/bin/env python
import re, random, os
import dbus, gobject
from threading import Timer
from dbus.mainloop.glib import DBusGMainLoop, threads_init
import setting

class PidginSMS:
	def recv_msg(self, account, sender, message, conversation, flags):
		message = self.strip_html(message)
		print sender, "said:", message
		self.conv = conversation
		if not self.Convs.has_key(self.conv):
			pass # pass we dont have any info about self.conv yet
		elif self.Convs[self.conv] == "ask" and message.upper()[0]=='Y':
			print "prepare to send sms.."
			self.t.cancel()
			self.send_sms(self.messages[self.conv])
			self.send_msg(self.conv, "SMS sent")
			self.Convs[self.conv] = "sent" 
			return			
		elif self.Convs[self.conv] == "ask" and message.upper()[0]=='N':
			self.t.cancel()
			self.Convs[self.conv] = "sent" 
			return			

		#starting timer for sending question about sms
		timeout = 60.0 * float(setting.readSettings()[1])
		if self.t == None and not self.Convs.has_key(self.conv):
			self.messages[self.conv] = [sender, message]
			self.t = Timer(timeout, self.timer_action)
			self.t.start()
		elif not self.t.isAlive() and not self.Convs.has_key(self.conv):
			self.messages[self.conv] = [sender, message]
			self.t.cancel()
			self.t = Timer(timeout, self.timer_action)
			self.t.start()
	def send_sms(self, message):
		s = setting.readSettings()
		username = s[2]
		passwd = s[3]
		sendNr = s[4]
		print "Sending SMS... from:",message[0],"containing:",message[1]
		os.system("""perl cellsynt.pl -d -u %s -p %s -m %s -r %s -O alpha -o pidignSMS""" % 
		          (username,passwd,message[0]+":"+message[1],sendNr))

	def timer_action(self):
		msg = setting.readSettings()[0]
		self.send_msg(self.conv, msg)
		self.Convs[self.conv] = "ask"
		
	def send_msg(self, conv, message):
		self.purple.PurpleConvImSend(self.purple.PurpleConvIm(conv),
		                             message)

	def strip_html(self, string):
		p = re.compile("<[^<]*?>")
		return p.sub("", string)

	def __init__(self):
		self.Convs = {}
		self.messages = {}
		self.t = None
		self.askingForSMS = False
		threads_init()
		dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
		threads_init()
		bus = dbus.SessionBus()
		
		obj = bus.get_object("im.pidgin.purple.PurpleService",
		                     "/im/pidgin/purple/PurpleObject")
		#object used for send messages and more
		self.purple = dbus.Interface(obj,
		                             "im.pidgin.purple.PurpleInterface")
		
		#Signal for incomming messages
		bus.add_signal_receiver(self.recv_msg,
					dbus_interface=
					"im.pidgin.purple.PurpleInterface",
					signal_name="ReceivedImMsg")
		status = self.purple.PurpleSavedstatusNew("", 5)
		self.purple.PurpleSavedstatusActivate(status)
	def main(self):
		loop = gobject.MainLoop()
		gobject.threads_init()
		loop.run()

if __name__ == "__main__":
	ps = PidginSMS()
	ps.main()

