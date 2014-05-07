"""thinkfast.py - executes EEG monitoring window.

Nilesh Kavthekar (github.com/nkav)
"""

import re
import time as tm
import random

from numpy import fft
import numpy as np

import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import gridspec

from realtime import data 

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def realfft(sampledata):
  return np.absolute(fft.rfft(sampledata))

def setupaxis(axn):
  axn.set_xlabel('Time (s)')
  axn.set_ylabel('Amplitude (V)')
  axn.grid(True)
  axn.set_title('RT EEG (Time Domain)')
  
def setupfftaxis(axis):
  ax4.set_xlabel('Frequency (Hz)')
  ax4.set_ylabel('Intensity')
  ax4.grid(True)
  ax4.set_title('RT EEG (Freq Domain)')
  ax4.axis([0, 30, 0, 15])

def dataline(axis, timedata, sampledata, symbol):
  return axis.plot(timedata, [3*i for i in sampledata], symbol)   

def setupdatalines():
  l1, = dataline(ax1, sampledata[0], sampledata[1], 'r-')
  l2, = dataline(ax2, sampledata[0], sampledata[2], 'b-')
  l3, = dataline(ax3, sampledata[0], sampledata[3], 'g-')
  return [l1, l2, l3]

def setupfftline():
  datasize = len(sampledata[0])
  timestep = (sampledata[0][-1] - sampledata[0][0])/datasize
  freqfft = fft.fftfreq(datasize, d=timestep)
  fftdat = realfft(sampledata[1])
  fftdat[0] = 0.0
  l4, = ax4.plot(freqfft[:40], fftdat[:40], 'b-') 
  return [l4]
  
def adjustaxistimes():
  timestart = sampledata[0][0]
  timeend = sampledata[0][-1]
  for axn in [ax1, ax2, ax3]:
    axn.axis([timestart, timeend, 0, 3.5])
 
def setupallaxes():
  for axn in [ax1, ax2, ax3]:
    setupaxis(axn)
  setupfftaxis(ax4)

def setupgrid():   
  ax1 = plt.subplot2grid((3,4), (0,0), colspan=2)
  ax2 = plt.subplot2grid((3,4), (1,0), colspan=2, sharex=ax1)
  ax3 = plt.subplot2grid((3,4), (2,0), colspan=2, sharex=ax1)
  ax4 = plt.subplot2grid((3,4), (0,2), colspan=2, rowspan=2)
  return (ax1, ax2, ax3, ax4)

def cleanupdata():
  for l in l13+l4:
    l.remove()

def p300():
  global learningperiod
  datasize = len(sampledata[0])
  timestep = (sampledata[0][-1] - sampledata[0][0])/datasize
  beg250 = int(.25 / timestep)
  end450 = int(.45 / timestep)
  beg600 = int(.60 / timestep)
  end700 = int(.70 / timestep)
  targetmean = np.mean(sampledata[1][beg250:end450])
  baselinemean = np.mean(sampledata[1][beg600:end700])
  newdatapoint = abs(float(targetmean - baselinemean))
  if learningperiod > 0:
    print 'Still learning...'
    pdata.append(newdatapoint)
    learningperiod -= 1
  elif learningperiod == 0:
    pdata.append(newdatapoint)
    print 'Think of a letter... any letter (from A to G)'
    tm.sleep(4)
    index = random.randint(0, 6)
    print 'Was it %s???? Lets see...' % alphabet[index] 
    learningperiod -= 1
  else:
    if newdatapoint > (np.mean(pdata) + np.std(pdata)):
      print 'We guessed right! You had a significant evoked response!' 
    else:
      pdata.append(newdatapoint)
      print 'Nope... doesnt look like it was. Were still learning!'
    print ' '
    print 'Think of a new letter... any letter (from A to G)'
    tm.sleep(2)
    index = random.randint(0, 6)
    print 'Was it %s???? Lets see...' % alphabet[index] 
  return pdata
 
pdata = []

if __name__ == '__main__':
  plt.ion()
  fig1 = plt.figure()
  ax1,ax2,ax3,ax4 = setupgrid()
  setupallaxes()
  fig1.tight_layout()
  plt.draw()
  learningperiod = 5
  while(1):
    try:
      sampledata = data() 
      adjustaxistimes()
      l13 = setupdatalines()
      l4 = setupfftline() 
      pdata = p300()
      fig1.tight_layout()
      plt.draw()
      cleanupdata()
    except:
      continue 
