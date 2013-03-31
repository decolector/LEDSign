#!/usr/bin/python
# vim: set ts=2 expandtab:

import serial
from JetFileII import Message


msg = Message.SetSystemTime()

print msg.encode('hex')

port = '/dev/ttyS0'
baudRate = 19200
ser = serial.Serial(port, baudRate)
x = ser.write(msg)
ser.close()
