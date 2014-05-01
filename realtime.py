import serial
import sys

def data(num):
  times = []
  fftdata1 = []
  fftdata2 = []
  fftdata3 = []
  ser = serial.Serial('/dev/tty.usbmodem1412')
  ### Dump remaining data from previous runs
  firstfound = False
  while (not firstfound):
    line = ser.readline() 
    try:
      values = [float(i) for i in line.rstrip('\r\n').split(',')]
      if(len(values) == 4):
        if(values[0] < 0.02):
          times.append(values[0])
          fftdata1.append(values[1])
          fftdata2.append(values[2])
          fftdata3.append(values[3])
          firstfound = True
    except:
      pass 
  ### Continue collecting sampled data
  for n in xrange(num):
    line = ser.readline() 
    try:
      values = [float(i) for i in line.rstrip('\r\n').split(',')]
      if(len(values) == 4):
        times.append(values[0])
        fftdata1.append(values[1])
        fftdata2.append(values[2])
        fftdata3.append(values[3])
    except:
      pass
  ser.close()
  return [times, fftdata1, fftdata2, fftdata3] 
