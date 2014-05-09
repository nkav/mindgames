import serial
import sys

SERIAL_PORT = '/dev/tty.usbmodem1412'

def data():
  ser = serial.Serial(SERIAL_PORT)
  ser.readline()
  ser.flush()
  start = False
  while not start: 
    line = ser.readline() 
    print "Stuck waiting for start"
    if line.rstrip('\r\n') == 'start!':
      print "Line is start!"
      start = True
    else:
      print line
  times = []
  fftdata1 = []
  fftdata2 = []
  fftdata3 = []
  ### Continue collecting sampled data
  ser.flush()
  try:
    line = ser.readline() 
    t = [float(i) for i in line.rstrip('\r\n').split(',')]
    line = ser.readline() 
    ch1 = [float(i) for i in line.rstrip('\r\n').split(',')]
    line = ser.readline() 
    ch2 = [float(i) for i in line.rstrip('\r\n').split(',')]
    line = ser.readline() 
    ch3 = [float(i) for i in line.rstrip('\r\n').split(',')]
    times = times + t
    fftdata1 = fftdata1 + ch1
    fftdata2 = fftdata2 + ch2
    fftdata3 = fftdata3 + ch3

    return [times, fftdata1, fftdata2, fftdata3] 
  except:
    pass  
