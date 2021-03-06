# vim: set ts=2 expandtab:
#******************************************************************************
#
# JetFileIIProtocol.py
# John O'Neil
# Saturday, March 9th 2013
#
# (simplified)JetfileII LED sign protocol derived off documentation
#
#******************************************************************************

import sys
import re
from struct import *
from time import localtime

class Animate:
  class Speed:
    Fastest = '\x0f0'
    VeryFast = '\x0f1'
    Fast = '\x0f2'
    Medium = '\x0f3'
    Slow = '\x0f4'
    VerySlow = '\x0f5'
    Slowest = '\x0f6'
  class Random:
    In = '\x0aI\x2f'
    Out = '\x0aO\x2f'
  class Jump:#'Jump' is really no "no animation" but None is a reserved keyword, so keeping 'jump'.
    In = '\x0aI\x30'
    Out = jump = '\x0aO\x30'
  class MoveLeft:
    In = '\x0aI\x31'
    Out = '\x0aO\x31'
  class MoveRight:
    In = '\x0aI\x32'
    Out = '\x0aO\x32'
  class WipeLeft:#called "scroll left" in documentation, but is really a wipe
    In = '\x0aI\x33'
    Out = '\x0aO\x33'
  class WipeRight:#called "scroll right" in documentation, but is really a wipe
    In = '\x0aI\x34'
    Out = '\x0aO\x34'
  class MoveUp:
    In = '\x0aI\x35'
    Out = '\x0aO\x35'
  class MoveDown:
    In = '\x0aI\x36'
    Out = '\x0aO\x36'
  class WipeHorizontalFromCenter:
    In = '\x0aI\x37'
    Out = '\x0aO\x37'
  class WipeUpward:
    In = '\x0aI\x38'
    Out = '\x0aO\x38'
  class WipeDownward:
    In = '\x0aI\x39'
    Out = '\x0aO\x39'
  class WipeHorizontalToCenter:
    In = '\x0aI\x3a'
    Out = '\x0aO\x3a'
  class WipeVerticalFromCenter:
    In = '\x0aI\x3b'
    Out = '\x0aO\x3b'
  class WipeVerticalToCenter:
    In = '\x0aI\x3c'
    Out = '\x0aO\x3c'
  class ShuttleFromLeftRight:
    In = '\x0aI\x3d'
    Out = '\x0aO\x3d'
  class ShuttleFromUpDown:
    In = '\x0aI\x3e'
    Out = '\x0aO\x3e'
  class PeelOffLeft:
    In = '\x0aI\x3f'
    Out = '\x0aO\x3f'
  class PeelOfRight:
    In = '\x0aI\x40'
    Out = '\x0aO\x40'
  class ShutterFromUpDown:
    In = '\x0aI\x41'
    Out = '\x0aO\x41'
  class ShutterFromLeftRight:
    In = '\x0aI\x42'
    Out = '\x0aO\x42'
  class Raindrops:
    In = '\x0aI\x43'
    Out = '\x0aO\x43'
  class RandomMosaic:
    In = '\x0aI\x44'
    Out = '\x0aO\x44'
  class TwinklingStars:
    In = '\x0aI\x45'
    Out = '\x0aO\x45'
  class HipHop:
    In = '\x0aI\x46'
    Out = '\x0aO\x46'
  class Radar:
    In = '\x0aI\x47'
    Out = '\x0aO\x47'
  class ToFourSides:
    In = '\x0aI\x34'
    Out = '\x0aO\x34'
  class FromFourSides:
    In = '\x0aI\x34'
    Out = '\x0aO\x34'
  class WipeOutFromFourBlocks:
    In = '\x0aI\x34'
    Out = '\x0aO\x34'
  class MoveOutFromFourBlocks:
    In = '\x0aI\x54'
    Out = '\x0aO\x54'
  class MoveInToFourBlocks:
    In = '\x0aI\x53'
    Out = '\x0aO\x53'
  class WipeFromULSquare:
    In = '\x0aI\x54'
    Out = '\x0aO\x54'
  class WipeFromLRSquare:
    In = '\x0aI\x55'
    Out = '\x0aO\x55'
  class WipeFromULSquare:
    In = '\x0aI\x56'
    Out = '\x0aO\x56'
  class WipeFromURSquare:
    In = '\x0aI\x57'
    Out = '\x0aO\x57'
  class WipeFromULSlant:
    In = '\x0aI\x58'
    Out = '\x0aO\x58'
  class WipeFromURSlant:
    In = '\x0aI\x59'
    Out = '\x0aO\x59'
  class WipeFromLLSlant:
    In = '\x0aI\x5a'
    Out = '\x0aO\x5a'
  class WipeFromLRSlant:
    In = '\x0aI\x5b'
    Out = '\x0aO\x5b'
  class MoveInFromULCorner:
    In = '\x0aI\x5c'
    Out = '\x0aO\x5c'
  class MoveInFromURCorner:
    In = '\x0aI\x5d'
    Out = '\x0aO\x5d'
  class MoveInFromLLCorner:
    In = '\x0aI\x5e'
    Out = '\x0aO\x5e'
  class MoveInFromLRCorner:
    In = '\x0aI\x5f'
    Out = '\x0aO\x5f'
  class GrowingUp:
    In = '\x0aI\x60'
    Out = '\x0aO\x60'
  
  class Pause:
    @staticmethod
    def Seconds(seconds):
      sec = int(seconds)
      #TODO: Better handling of seconds values greater than 99
      return '\x0e0{0:02d}'.format(sec)

class Format:
  NewFrame = '\x0c'
  NewLine = '\x0d'
  Halfspace = '\x82'
  class Temperature:
    Celsius = '\x0b\x31'
    Farenheit = '\x0b\x33'
    Humidity = '\x0b\x32'
  @staticmethod
  def Linespace(space):
    if space<0 or space > 9:
      return Linespace(0)
    else:
      return '\x08' + str(space)
  class Flash:
    On = '\x071'
    Off = '\x070'
  class AutoTypeset:
    Off = '\x1b0a'
    On = '\x1b0b'
  class Background:
    Black = '\x1d0'
    Red = '\x1d1'
    Green = '\x1d2'
    Amber = '\x1d3'
  class Align:
    class Vertical:
      Center = '\x1f0'
      Top = '\x1f1'
      Bottom = '\x1f2'
    class Horizontal:
      Center = '\x1e0'
      Left = '\x1e1'
      Right = '\x1e2'
  class ExtendedAscii:
    Insert = '\x17'
  @staticmethod
  def InterpretMarkup(text):
    #replace entries in curly brackets by their proper protocol values
    #e.g. 'hello {Format.NewLine} There' will insert Format.NewLine binary in place of curly brackets markup.
    def ReplaceMarkupTagWithArg(match):
      code = match.group(1).strip().lower()
      arg = match.group(2).strip().lower()
      #print "code: " + code +" arg: " + arg
      if code in Markup.Registry:
        #pass
        return Markup.Registry[code](arg)
      return match.group(0)
    def ReplaceMarkupTags(match):
      code = match.group(1).strip().lower()
      #print "code is " + code
      if code in Markup.Registry:
          return Markup.Registry[code]
      return match.group(0)
    
    regex_with_arg = re.compile(r"\{(.*?)=(.*?)\}")
    regex = re.compile(r"\{(.*?)\}")
    text = re.sub(regex_with_arg, ReplaceMarkupTagWithArg, text)
    text = re.sub(regex, ReplaceMarkupTags, text)
    #print "subbed text: " + text
    return text

class Date:
  class MMDDYY:
    WithForwardSlashes = '\x0b\x20'
    WithDashes = '\x0b\x22'
    WithDots = '\x0b\x24'
  class DDMMYY:
    WithForwardSlashes = '\x0b\x21'
    WithDashes = '\x0b\x23'
  YY = '\x0b\x25'
  YYYY = '\x0b\x26'
  class Month:
    Number = '\x0b\x27'
    Abbreviation = '\x0b\x28'
  Day = '\x0b\x29'#day of month as two digit number
  class DayOfWeek:
    Number = '\x0b\x2a'
    Abbreviation = '\x0b\x2b'
  class Time:
    HH = '\x0b\x2c'
    MIN = '\x0b\x2d'
    SEC = '\x0b\x2e'
    HHMIN23hr = '\x0b\x2f'
    HHMIN12hr = '\x0b\x30'

#picture handling is described in protocol section 4
class Picture:
  @staticmethod
  def FromDiskFilename(filename,disk='E'):
    return '\x14'+disk+filename
  

class Font:
  n5x5 = '\x1a0'
  n7x6 = '\x1a1'
  n14x8 = '\x1a2'
  n15x9 = '\x1a3'
  n16x9 = '\x1a4'
  n24x16 = '\x1a6'
  n11x9 = '\x1a:'
  n12x7 = '\x1a;'
  n22x18 = '\x1a<'
  n30x18 = '\x1a+'
  n40x21 = '\x1a>'
  b14x10 = '\x1aN'
  b15x10 = '\x1aO'
  b16x12 = '\x1aP'
  b24x8 = '\x1aQ'
  b32x8 ='\x1aR'
  b11x7 = '\x1aS'
  b12x7 = '\x1aT'
  b22x12 = '\x1aU'
  b40x21 = '\x1aV'
  class Color:
    Black = '\x1c\x30'
    Red = '\x1c\x31'
    Green = '\x1c\x32'
    Amber = '\x1c\x33'
    class Mixed:
      Characters = '\x1c\x34'
      Horizontal = '\x1c\x35'
      Wave = '\x1c\x36'
      Splash = '\x1c\x37'

#See section 3.1 of protocol description
class Message:
  Header = '\x00\x00\x00\x00\x00\x01Z00'
  Type2Header = 'QZ00SAX'
  Protocol = '\x06'
  BeginCommand = '\x02'
  WriteFile = 'A'
  Coda = '\x04'
  SYN = '\x55\xa7'
  class DisplayControlWithoutChecksum:
    @staticmethod
    def Create(msgId, unit_address=0, disk='E', folder='T', text='Testing, 1, 2, 3.'):
      p = Message.DisplayControlWithoutChecksum
      f = Format
      m = Message
      return m.Header + m.BeginCommand + m.WriteFile + m.MsgId2DiskFolderFilename(msgId) + m.Protocol + f.InterpretMarkup(text) + m.Coda
  @staticmethod
  def MsgId2Filename(msgId):
    #asciiMajor = 65 + int(msgId/26)
    #asciiMinor = 65 + int(msgId % 26)
    #return '{0:01c}{0:01c}'.format(asciiMajor,asciiMinor)
    return str('%c%c' % (65 + int(msgId / 26), 65 + (msgId % 26)))
  @staticmethod
  def MsgId2DiskFolderFilename(msgId,disk='E',folder='T'):
    #print "MsgId2DiskFolderFilename returns filename " + Message.MsgId2Filename(msgId)
    return '\x0f' + disk + folder + Message.MsgId2Filename(msgId)

  @staticmethod
  def Checksum(message):
    sum = 0
    for c in message:
      sum = sum + ord(c)
    #print "checksum calculated is " + str(sum)
    USHRT_MAX = 65535
    packed =  pack('H',sum % USHRT_MAX)
    #print packed
    return packed

  @staticmethod
  def Create(msg):
    return Message.Type2Header + Format.InterpretMarkup(msg) + Message.Coda
    #return Message.Type2Header + msg + Message.Coda

  @staticmethod
  def FileLabel(label):
    if(len(label) < 12):
      return label.ljust(12,'\x00')
    elif (len(label) > 12):
      return label[:12]
    return label

  @staticmethod
  def WriteText(message,disk_partition='E',buzzer_time=0,file_label='AB'):
    #build and return an emergency message with checksum backwards from data
    m = Message.Create(message)
    data_length = len(m)
    m = pack('L',data_length) +  pack('H',data_length) + pack('H',1) + pack('H',1) + m
    m = disk_partition + pack('B',buzzer_time) + Message.FileLabel(file_label) + m
    m = '\x00' + m;#flag
    m = '\x06' + m;#arglength (arg is 1x4 bytes long)
    m = '\x04' + m;#subcommand
    m = '\x02' + m;#main command
    m = '\xab\xcd' + m;#packet serial
    m = '\x00' + m;#source, dest addresses.
    m = '\x00' + m;
    m = '\x00' + m;
    m = '\x00' + m;
    m = pack('H',data_length) + m;
    m = Message.Checksum(m) + m;
    m = Message.SYN + m;
    return m

  @staticmethod
  def WriteSystemFile(file_contents, file_label='SEQUENT.SYS'):
    #build and return an emergency message with checksum backwards from data
    m = file_contents #Message.Create(message)
    data_length = len(m)
    m = pack('L',data_length) +  pack('H',data_length) + pack('H',1) + pack('H',1) + pack('H',0) + m
    m = Message.FileLabel(file_label) + m
    m = '\x00' + m;#flag
    m = '\x06' + m;#arglength (arg is 1x4 bytes long)
    m = '\x02' + m;#subcommand
    m = '\x02' + m;#main command
    m = '\xab\xcd' + m;#packet serial
    m = '\x00' + m;#source, dest addresses.
    m = '\x00' + m;
    m = '\x00' + m;
    m = '\x00' + m;
    m = pack('H',data_length) + m;
    m = Message.Checksum(m) + m;
    m = Message.SYN + m;
    return m

  @staticmethod
  def SetSystemTime():
    data_length = 0
    current_time = localtime()
    year = int(str(current_time[0]),base=16)
    month = int(str(current_time[1]),base=16)
    day = int(str(current_time[2]),base=16)
    hour = int(str(current_time[3]),base=16)
    minute = int(str(current_time[4]),base=16)
    dow = int(str(current_time[6]),base=16)
    timezone = 0
    m = ''
    m = pack('H',year) + pack('B',month) + pack('B',day) + pack('B',hour) + pack('B',minute) + pack('B',dow) + pack('B',timezone) + m
    m = '\x00' + m;#flag
    m = '\x02' + m;#arglength (arg is 1x4 bytes long)
    m = '\x02' + m;#subcommand
    m = '\x05' + m;#main command
    m = '\xab\xcd' + m;#packet serial
    m = '\x00' + m;#source, dest addresses.
    m = '\x00' + m;
    m = '\x00' + m;
    m = '\x00' + m;
    m = pack('H',data_length) + m;
    m = Message.Checksum(m) + m;
    m = Message.SYN + m;
    return m

  class File:
    def __init__(self,data,file_label='AB',filetype='T',partition='E'):
      self.file_label=Message.FileLabel(file_label)
      #print "File label: " + self.file_label + " "+ self.file_label.encode('hex')
      self.data=Message.WriteText(data,file_label=file_label,disk_partition=partition)
      self.filetype=filetype

  @staticmethod
  def Playlist(files, partition='E', file_label='SEQUENT.SYS'):
    #build and return an emergency message with checksum backwards from data
    num_files = len(files)
    m = 'SQ' + '\x04' + '\x00' + pack('H', num_files) + pack('H',0x0)
    for file in files:
      m = m + partition + file.filetype + '\x0f' + Message.WeekRepetition()
      m = m + Message.DateTimeStructure(year=2008,month=3,day=16,hour=0,minute=0) + Message.DateTimeStructure(year=2008,month=3,day=16,hour=0,minute=0)
      #m = m + Message.Checksum(file.data) + pack('H',len(file.data)) + file.file_label
      m = m +'\xb0\x00' + '\x00\x00' + file.file_label
    return m

  @staticmethod
  def StringFile(data, partition='E',file_label="string.txt"):
    #build and return an emergency message with checksum backwards from data
    messages = []
    data_size = len(data)
    num_messages = data_size/1024 + 1
    payload_size = data_size/num_messages
    for imsg in range(num_messages):
      m = data[imsg*payload_size:imsg*payload_size+payload_size] #Message.Create(message)
      data_length = len(m)
      m = partition + pack('B',0) +  Message.FileLabel(file_label) + pack('L',data_size) + pack('H',payload_size) + pack('H',num_messages) + pack('H',imsg+1) + m
      m = '\x00' + m;#flag
      m = '\x06' + m;#arglength (arg is 1x4 bytes long)
      m = '\x05' + m;#subcommand
      m = '\x02' + m;#main command
      m = '\xab\xcd' + m;#packet serial
      m = '\x00' + m;#source, dest addresses.
      m = '\x00' + m;
      m = '\x00' + m;
      m = '\x00' + m;
      m = pack('H',data_length) + m;
      m = Message.Checksum(m) + m;
      m = Message.SYN + m;
      if(num_messages is 1):
        return m
      messages.append(m)
    return messages   

  @staticmethod
  def Picture(data, partition='E',file_label="AA"):
    #build and return an emergency message with checksum backwards from data
    messages = []
    data_size = len(data)
    num_messages = data_size/512 + 1
    payload_size = data_size/num_messages
    for imsg in range(num_messages):
      m = data[imsg*payload_size:imsg*payload_size+payload_size] #Message.Create(message)
      data_length = len(m)
      m = partition + pack('B',0) +  Message.FileLabel(file_label) + pack('L',data_size) + pack('H',payload_size) + pack('H',num_messages) + pack('H',imsg+1) + m
      m = '\x00' + m;#flag
      m = '\x06' + m;#arglength (arg is 1x4 bytes long)
      m = '\x06' + m;#subcommand
      m = '\x02' + m;#main command
      m = '\xab\xcd' + m;#packet serial
      m = '\x00' + m;#source, dest addresses.
      m = '\x00' + m;
      m = '\x00' + m;
      m = '\x00' + m;
      m = pack('H',data_length) + m;
      m = Message.Checksum(m) + m;
      m = Message.SYN + m;
      messages.append(m)
    return messages   

  @staticmethod
  def DateTimeStructure(year=0,month=0,day=0,hour=0,minute=0):
    return pack('H',year) + pack('B',month) + pack('B',day) + pack('B',hour) + pack('B',minute) + '\x01' +'\x01'

  @staticmethod
  def WeekRepetition():
    return str('\x80')
  

  @staticmethod
  def EmergencyMessage(msg,t=10):
    #build and return an emergency message with checksum backwards from data
    m = Message.Create(msg);
    data_length = len(m)
    m = pack('H',1) + '\x00' + '\x00' + m;#time, sound, reserved
    m = '\x00' + m;#flag
    m = '\x01' + m;#arglength (arg is 1x4 bytes long)
    m = '\x09' + m;#subcommand
    m = '\x02' + m;#main command
    m = '\xab\xcd' + m;#packet serial
    m = '\x00' + m;#source, dest addresses.
    m = '\x00' + m;
    m = '\x00' + m;
    m = '\x00' + m;
    m = pack('H',data_length) + m;
    m = Message.Checksum(m) + m;
    m = Message.SYN + m;
    return m

  @staticmethod
  def TurnSignOff(goodbyeMsg=False):
    #build and return an emergency message with checksum backwards from data
    m = ''
    data_length = 0
    if goodbyeMsg:
      m = pack('L',0) + m
    else:
      m = pack('L',1) + m
    m = '\x00' + m;#flag
    m = '\x01' + m;#arglength (arg is 1x4 bytes long)
    m = '\x03' + m;#subcommand
    m = '\x04' + m;#main command
    m = '\xab\xcd' + m;#packet serial
    m = '\x00' + m;#source, dest addresses.
    m = '\x00' + m;
    m = '\x00' + m;
    m = '\x00' + m;
    m = pack('H',data_length) + m;
    m = Message.Checksum(m) + m;
    m = Message.SYN + m;
    return m

  @staticmethod
  def TurnSignOn():
    #build and return an emergency message with checksum backwards from data
    m = ''
    data_length = 0
    m = '\x00' + m;#flag
    m = '\x00' + m;#arglength (arg is 1x4 bytes long)
    m = '\x04' + m;#subcommand
    m = '\x04' + m;#main command
    m = '\xab\xcd' + m;#packet serial
    m = '\x00' + m;#source, dest addresses.
    m = '\x00' + m;
    m = '\x00' + m;
    m = '\x00' + m;
    m = pack('H',data_length) + m;
    m = Message.Checksum(m) + m;
    m = Message.SYN + m;
    return m

  @staticmethod
  def StartCountdown(day=0,hour=0,minute=0,second=0):
    #build and return an emergency message with checksum backwards from data
    m = ''
    data_length = 0
    m = pack('B',day) + pack('B',hour) + pack('B',minute) + pack('B',second) + m
    m = '\x00' + m;#flag
    m = '\x01' + m;#arglength (arg is 1x4 bytes long)
    m = '\x11' + m;#subcommand
    m = '\x06' + m;#main command
    m = '\xab\xcd' + m;#packet serial
    m = '\x00' + m;#source, dest addresses.
    m = '\x00' + m;
    m = '\x00' + m;
    m = '\x00' + m;
    m = pack('H',data_length) + m;
    m = Message.Checksum(m) + m;
    m = Message.SYN + m;
    return m

  @staticmethod
  def StopCountdown():
    #build and return an emergency message with checksum backwards from data
    m = ''
    data_length = 0
    m = '\x00' + m;#flag
    m = '\x00' + m;#arglength (arg is 1x4 bytes long)
    m = '\x12' + m;#subcommand
    m = '\x06' + m;#main command
    m = '\xab\xcd' + m;#packet serial
    m = '\x00' + m;#source, dest addresses.
    m = '\x00' + m;
    m = '\x00' + m;
    m = '\x00' + m;
    m = pack('H',data_length) + m;
    m = Message.Checksum(m) + m;
    m = Message.SYN + m;
    return m

  @staticmethod
  def DynamicDisplay(ledData):
    #build and return an arra of messages (of same size)
    #that describe the display we want.
    #1 how many messages will we create?
    num_messages = len(ledData)/512
    data_length = 512
    message_array = []
    for iMsg in range(num_messages):
      start = iMsg*512
      end = start + 512
      m = ledData[start:end]
      m = pack('H', data_length) + pack('H',num_messages) + pack('H', iMsg+1) + pack('H',0) + m
      m = '\x00' + m;#flag
      m = '\x02' + m;#arglength (arg is 2x4 bytes long)
      m = '\x04' + m;#subcommand
      m = '\x08' + m;#main command
      m = '\xab\xcd' + m;#packet serial
      m = '\x00' + m;#source, dest addresses.
      m = '\x00' + m;
      m = '\x00' + m;
      m = '\x00' + m;
      m = pack('H',data_length) + m;
      m = Message.Checksum(m) + m;
      m = Message.SYN + m;
      message_array.append(m)
    return message_array

  class Bitmap:
    CommmandCharacter = 'I'
    @staticmethod
    def Create(filename,bytes,unit_address=0,disk='E'):
      p = Message.Bitmap
      f = Format
      m = Message
      return m.Header + m.BeginCommand + p.CommandCharacter + filename + bytes + m.Coda
 
#There's gotta be a better way than this...
class Markup:
  Registry = {
    'pause' : Animate.Pause.Seconds(0), #force no pause, shame on me
    'nl' : Format.NewLine,
    'newframe' : Format.NewFrame,
    'halfspace' : Format.Halfspace,
    'flashon' : Format.Flash.On,
    'flashoff' : Format.Flash.Off,
    'red' : Font.Color.Red,
    'green' : Font.Color.Green,
    'amber' : Font.Color.Amber,
    'top' : Format.Align.Vertical.Top,
    'middle' : Format.Align.Vertical.Center,
    'bottom' : Format.Align.Vertical.Bottom,
    'left' : Format.Align.Horizontal.Left,
    'center' : Format.Align.Horizontal.Center,
    'right' : Format.Align. Horizontal.Right,
    'typeseton' : Format.AutoTypeset.On,
    'typesetoff' : Format.AutoTypeset.Off,
    'extascii': Format.ExtendedAscii.Insert,
    'slowest' : Animate.Speed.Slow,
    'veryslow' : Animate.Speed.VerySlow,
    'slow' : Animate.Speed.Slow,
    'medium' : Animate.Speed.Medium,
    'fast' : Animate.Speed.Fast,
    'veryFast' : Animate.Speed.VeryFast,
    'fastest' : Animate.Speed.Fastest,
    'nonein' : Animate.Jump.In,
    'noneout' : Animate.Jump.Out,
    'moveleftin' : Animate.MoveLeft.In,
    'moveleftout' : Animate.MoveLeft.Out,
    'moverightin' : Animate.MoveRight.In,
    'moverightout' : Animate.MoveRight.Out,
    'wipeleftin' : Animate.WipeLeft.In,
    'wiperightin' : Animate.WipeRight.In,
    'moveupin' : Animate.MoveUp.In,
    'movedownin' : Animate.MoveDown.In,
    'wipehorizontalfromcenterin' : Animate.WipeHorizontalFromCenter.In,
    'wipeupwardin' : Animate.WipeUpward.In,
    'wipedownwardin' : Animate.WipeDownward.In,
    'wipehorizontaltocenterin' : Animate.WipeHorizontalToCenter.In,
    'wipeverticalfromcenterin' : Animate.WipeVerticalFromCenter.In,
    'wipeverticaltocenterin' : Animate.WipeVerticalToCenter.In,
    'shuttlefromleftrightin' : Animate.ShuttleFromLeftRight.In,
    'shuttlefromupdownin' : Animate.ShuttleFromUpDown.In,
    'peeloffleftin' : Animate.PeelOffLeft.In,
    'peeloffright' : Animate.PeelOfRight.In,
    'shutterfromupdownin' : Animate.ShutterFromUpDown.In,
    'shutterfromleftrightin' : Animate.ShutterFromLeftRight.In,
    'raindropsin' : Animate.Raindrops.In,
    'randommosaicin' : Animate.RandomMosaic.In,
    'twinklingstarsin' : Animate.TwinklingStars.In,
    'hiphopin' : Animate.HipHop.In,
    'radarin' : Animate.Radar.In,
    'tofoursidesin' : Animate.ToFourSides.In,
    'fromfoursidesin' : Animate.FromFourSides.In,
    'wipeoutfromfourblocksin' : Animate.WipeOutFromFourBlocks.In,
    'moveoutfromfourblocksin' : Animate.MoveOutFromFourBlocks.In,
    'moveintofourblocksin' : Animate.MoveInToFourBlocks.In,
    'wipefromulsquarein' : Animate.WipeFromULSquare.In,
    'wipefromlrsquarein' : Animate.WipeFromLRSquare.In,
    'wipefromulsquarein' : Animate.WipeFromULSquare.In,
    'wipefromursquarein' : Animate.WipeFromURSquare.In,
    'wipefromulslantin' : Animate.WipeFromULSlant.In,
    'wipefromurslantin' : Animate.WipeFromURSlant.In,
    'wipefromllslantin' : Animate.WipeFromLLSlant.In,
    'wipefromlrslantin' : Animate.WipeFromLRSlant.In,
    'moveinfromulcornerin' : Animate.MoveInFromULCorner.In,
    'moveinfromurcornerin' : Animate.MoveInFromURCorner.In,
    'moveinfromllcornerin' : Animate.MoveInFromLLCorner.In,
    'moveinfromlrcornerin' : Animate.MoveInFromLRCorner.In,
    'growingupout' : Animate.GrowingUp.In,
    'wipeleftout' : Animate.WipeLeft.In,
    'wiperightout' : Animate.WipeRight.Out,
    'moveupout' : Animate.MoveUp.Out,
    'movedownout' : Animate.MoveDown.Out,
    'wipehorizontalfromcenterout' : Animate.WipeHorizontalFromCenter.Out,
    'wipeupwardout' : Animate.WipeUpward.Out,
    'wipedownwardout' : Animate.WipeDownward.Out,
    'wipehorizontaltocenterout' : Animate.WipeHorizontalToCenter.Out,
    'wipeverticalfromcenterout' : Animate.WipeVerticalFromCenter.Out,
    'wipeverticaltocenterout' : Animate.WipeVerticalToCenter.Out,
    'shuttlefromleftrightout' : Animate.ShuttleFromLeftRight.Out,
    'shuttlefromupdownout' : Animate.ShuttleFromUpDown.Out,
    'peeloffleftout' : Animate.PeelOffLeft.Out,
    'peeloffright' : Animate.PeelOfRight.Out,
    'shutterfromupdownout' : Animate.ShutterFromUpDown.Out,
    'shutterfromleftrightout' : Animate.ShutterFromLeftRight.Out,
    'raindropsout' : Animate.Raindrops.Out,
    'randommosaicout' : Animate.RandomMosaic.Out,
    'twinklingstarsout' : Animate.TwinklingStars.Out,
    'hiphopout' : Animate.HipHop.Out,
    'radarout' : Animate.Radar.Out,
    'tofoursidesout' : Animate.ToFourSides.Out,
    'fromfoursidesout' : Animate.FromFourSides.Out,
    'wipeoutfromfourblocksout' : Animate.WipeOutFromFourBlocks.Out,
    'moveoutfromfourblocksout' : Animate.MoveOutFromFourBlocks.Out,
    'moveintofourblocksout' : Animate.MoveInToFourBlocks.Out,
    'wipefromulsquareout' : Animate.WipeFromULSquare.Out,
    'wipefromlrsquareout' : Animate.WipeFromLRSquare.Out,
    'wipefromulsquareout' : Animate.WipeFromULSquare.Out,
    'wipefromursquareout' : Animate.WipeFromURSquare.Out,
    'wipefromulslantout' : Animate.WipeFromULSlant.Out,
    'wipefromurslantout' : Animate.WipeFromURSlant.Out,
    'wipefromllslantout' : Animate.WipeFromLLSlant.Out,
    'wipefromlrslantout' : Animate.WipeFromLRSlant.Out,
    'moveinfromulcornerout' : Animate.MoveInFromULCorner.Out,
    'moveinfromurcornerout' : Animate.MoveInFromURCorner.Out,
    'moveinfromllcornerout' : Animate.MoveInFromLLCorner.Out,
    'moveinfromlrcornerout' : Animate.MoveInFromLRCorner.Out,
    'growingupout' : Animate.GrowingUp.Out,
    '5x5' : Font.n5x5,
    '7x6' : Font.n7x6,
    '12x7' : Font.n12x7,
    '16x9' : Font.n16x9,
    '22x18' : Font.n22x18,
    'b12x7' : Font.b12x7,
    'b16x12' : Font.b16x12,
    'b22x12' : Font.b22x12,
    'b32x8' : Font.b32x8,
    'mm/dd/yy':Date.MMDDYY.WithForwardSlashes,
    'mm-dd-yy':Date.MMDDYY.WithDashes,
    'mm.dd.yy':Date.MMDDYY.WithDots,
    'dd/mm/yy':Date.DDMMYY.WithForwardSlashes,
    'dd-mm-yy':Date.DDMMYY.WithDashes,
    'yy':Date.YY,
    'yyyy':Date.YYYY,
    'month_num':Date.Month.Number,
    'month_abbr':Date.Month.Abbreviation,
    'date':Date.Day,
    'dow_number':Date.DayOfWeek.Number,
    'dow_abbr':Date.DayOfWeek.Abbreviation,
    'hh':Date.Time.HH,
    'min':Date.Time.MIN,
    'sec':Date.Time.SEC,
    'hhmin_23hr':Date.Time.HHMIN23hr,
    'hhmin_12hr':Date.Time.HHMIN12hr,
    'celsius':Format.Temperature.Celsius,
    'farenheit':Format.Temperature.Farenheit,
    'humidity':Format.Temperature.Humidity 
  } 
  

