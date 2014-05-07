import serial
import sys

SERIAL_PORT = '/dev/ttyACM0'

def data():
  ser = serial.Serial(SERIAL_PORT)
  while(1):
    times = []
    fftdata1 = []
    fftdata2 = []
    fftdata3 = []
    ### Continue collecting sampled data
    start = False
    while not start: 
      line = ser.readline() 
      if line.rstrip('\r\n') == 'start!':
        start = True
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
