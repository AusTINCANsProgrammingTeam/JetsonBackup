#!/usr/bin/env python

import logging
import time
from networktables import NetworkTables

logging.basicConfig(level=logging.DEBUG)

def valueChanged(table, key, value, isNew):
   print("%s=%s, IsNew?=%s" % (key, value, isNew))

def connected(connected, info):
   print (info, "; Connected=%s" % connected)


NetworkTables.initialize(server='10.21.58.18')
NetworkTables.addConnectionListener(connected, immediateNotify=True)
nt = NetworkTables.getTable("SmartDashboard")
nt.addEntryListener(valueChanged)

while True:
   print("X=", nt.getNumber('X', 0))
   time.sleep(1)
