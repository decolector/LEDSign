#!/usr/bin/python
# vim: set ts=2 expandtab:

import serial
from JetFileII import Message


msg = Message.StopCountdown()

#print msg.encode("hex")

#print 'size of message is ' + str(len(msg))

port = '/dev/ttyS0'
baudRate = 19200
ser = serial.Serial(port, baudRate)
x = ser.write(msg)
ser.close()
