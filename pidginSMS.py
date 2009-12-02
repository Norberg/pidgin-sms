#!/usr/bin/env python
import re, random
import dbus, gobject
from threading import Timer
from dbus.mainloop.glib import DBusGMainLoop, threads_init

class PidginSMS:
	def recv_msg(self, account, sender, message, conversation, flags):
		message = self.strip_html(message)
		print sender, "said:", message
		self.conv = conversation
		#print "DEBUG: message: ", message,
		#print " self.askingForSMS: ", self.askingForSMS,
		#print " self.t", self.t
		#to send or not to send an SMS
		if self.askingForSMS and message.upper()[0] == 'Y':
			print "prepare to send sms.."
			self.t.cancel()
			self.send_sms()
			self.send_msg(self.conv, "SMS sent")
			#self.askingForSMS = False
			return			
		elif self.askingForSMS:
			print "prepare to not send sms.. due to:", message.upper()[0]
			self.t.cancel()
			#self.askingForSMS = False
			return			

		#starting timer for sending question about sms
		if self.t == None and not self.askingForSMS:
			self.askingForSMS = True
			self.t = Timer(4.0, self.timer_action)
			self.t.start()
		elif not self.askingForSMS:
			self.askingForSMS = True
			self.t.cancel()
			self.t = Timer(4.0, self.timer_action)
			self.t.start()
	def send_sms(self):
		print "Sending SMS..."

	def timer_action(self):
		msg = "Im not at my computer atm, would you like to send" + \
		      " me the message as an sms instead Y/N?"
		self.send_msg(self.conv, msg)
		
	def send_msg(self, conv, message):
		self.purple.PurpleConvImSend(self.purple.PurpleConvIm(conv),
		                             message)

	def strip_html(self, string):
		p = re.compile("<[^<]*?>")
		return p.sub("", string)

	def __init__(self):
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
	def main(self):
		loop = gobject.MainLoop()
		gobject.threads_init()
		loop.run()

if __name__ == "__main__":
	ps = PidginSMS()
	ps.main()

