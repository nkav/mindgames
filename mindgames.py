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
from matplotlib.mlab import PCA

from realtime import data 
import game

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
random.shuffle(alphabet)

alphabetindex = 0

def realfft(sampledata):
  return np.absolute(fft.rfft(sampledata))

def setupaxis(axn):
  axn.set_xlabel('Time (s)')
  axn.set_ylabel('Amplitude (V)')
  axn.grid(True)
  axn.set_title('RT EEG (Time Domain)')
  
def setupfftaxis():
  ax4.set_xlabel('Frequency (Hz)')
  ax4.set_ylabel('Intensity')
  ax4.grid(True)
  ax4.set_title('RT EEG (Freq Domain)')
  ax4.axis([0, 30, 0, 15])

def setuppcaaxis():
  pcaarr = np.array(results.Y).transpose()
  pcax = pcaarr[0, :] 
  pcay = pcaarr[1, :] 
  ax5.grid(True)
  ax5.set_title('3-Variable Principle Component Analysis')
  ax5.axis([-1.0, 2.5, -0.5, 0.5])
  l7 = ax5.scatter(pcax, pcay, s=40,  marker='o')
  return l7
  

def dataline(axis, timedata, sampledata, symbol):
  return axis.plot(timedata, [3*i for i in sampledata], symbol)   

def setupdatalines():
  l1, = dataline(ax1, sampledata[0], sampledata[1], 'r-')
  l2, = dataline(ax2, sampledata[0], sampledata[2], 'b-')
  l3, = dataline(ax3, sampledata[0], sampledata[3], 'g-')
  return [l1, l2, l3]

def setupfftline():
  fftdat1 = realfft(sampledata[1])
  fftdat2 = realfft(sampledata[2])
  fftdat3 = realfft(sampledata[3])
  fftdat1[0] = 0.0
  fftdat2[0] = 0.0
  fftdat3[0] = 0.0
  return (fftdat1[:40],fftdat2[:40],fftdat3[:40])

def plotfft():
  datasize = len(sampledata[0])
  timestep = (sampledata[0][-1] - sampledata[0][0])/datasize
  freqfft = fft.fftfreq(datasize, d=timestep)
  l4, = ax4.plot(freqfft[:40], fft1, 'r-') 
  l5, = ax4.plot(freqfft[:40], fft2, 'b-') 
  l6, = ax4.plot(freqfft[:40], fft3, 'g-') 
  return [l4, l5, l6]
 
def adjustaxistimes():
  timestart = sampledata[0][0]
  timeend = sampledata[0][-1]
  for axn in [ax1, ax2, ax3]:
    axn.axis([timestart, timeend, 0, 3.5])

def PCAanalysis():
  fftarray = np.array([fft1, fft2, fft3])
  results = PCA(fftarray.transpose())
  return results
 
def setupallaxes():
  for axn in [ax1, ax2, ax3]:
    setupaxis(axn)
  setupfftaxis()

def setupgrid():   
  ax1 = plt.subplot2grid((3,4), (0,0), colspan=2)
  ax2 = plt.subplot2grid((3,4), (1,0), colspan=2, sharex=ax1)
  ax3 = plt.subplot2grid((3,4), (2,0), colspan=2, sharex=ax1)
  ax4 = plt.subplot2grid((3,4), (0,2), colspan=2 )
  ax5 = plt.subplot2grid((3,4), (1,2), colspan=2, rowspan=2)
  return (ax1, ax2, ax3, ax4, ax5)

def cleanupdata():
  for l in l13+l46:
    l.remove()
  l7.remove()

def guessnewletter():
  global alphabetindex
  alphabetindex += 1
  alphabetindex %= 7
  return alphabet[alphabetindex] 

def p300(guessletter):
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
    text0 = "still learning..." + str(learningperiod)
    game.writetk(text0)
    pdata.append(newdatapoint)
    learningperiod -= 1
  elif learningperiod == 0:
    pdata.append(newdatapoint)
    learningperiod -= 1
  else:
    if newdatapoint > (np.mean(pdata) + np.std(pdata)):
      game.addlinetk('We guessed right! You had a significant evoked response!')
      game.writeletter(guessletter)
      game.addlinetk('Now think of a new letter...')
      tm.sleep(5)
    else:
      pdata.append(newdatapoint)
      game.addlinetk('Nope... doesnt look like it was. Were still learning!')
      game.addlinetk('Keep thinking of that letter!')
      tm.sleep(5)
  return pdata
 
pdata = []

if __name__ == '__main__':
  plt.ion()
  fig1 = plt.figure()
  mng = plt.get_current_fig_manager()
  mng.window.state('zoomed')
  ax1,ax2,ax3,ax4,ax5 = setupgrid()
  setupallaxes()
  fig1.tight_layout()
  plt.draw()
  learningperiod = 15
  while(1):
    try:
      lettertoprint = None
      if learningperiod < 0:
        game.writetk("Think of a letter (anything from A -> G)")
        lettertoprint = guessnewletter()
        tm.sleep(5)
        game.inlinetk("Was it... ")
        tm.sleep(1)
        learningperiod0 = lettertoprint*5 + '???? Lets see...'
        game.addlinetk(learningperiod0)
      sampledata = data() 
      adjustaxistimes()
      l13 = setupdatalines()
      fft1, fft2, fft3 = setupfftline() 
      l46 = plotfft()
      pdata = p300(lettertoprint)
      results = PCAanalysis()
      l7 = setuppcaaxis() 
      fig1.tight_layout()
      plt.draw()
      cleanupdata()
    except:
      continue
