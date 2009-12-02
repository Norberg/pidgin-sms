#!/usr/bin/env python
from StartGTK import *
import pidginSMS
GUI = StartGTK()
gtk.gdk.threads_init()
pidginSMS.PidginSMS()
gtk.main()
