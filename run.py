#!/usr/bin/env python
# Copyright 2009 Simon Norberg
from StartGTK import *
import pidginSMS
GUI = StartGTK()
gtk.gdk.threads_init()
pidginSMS.PidginSMS()
gtk.main()
