import re
import time as tm
from numpy import fft
import numpy as np
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import gridspec
from realtime import data 

def realfft(sampledata):
  return np.absolute(fft.rfft(sampledata))

if __name__ == '__main__':
  plt.ion()
  fig1 = plt.figure()
  ax1 = plt.subplot2grid((3,4), (0,0), colspan=2)
  ax2 = plt.subplot2grid((3,4), (1,0), colspan=2, sharex=ax1)
  ax3 = plt.subplot2grid((3,4), (2,0), colspan=2, sharex=ax1)
  ax4 = plt.subplot2grid((3,4), (0,2), colspan=2, rowspan=2)
  for axn in [ax1, ax2, ax3]:
    axn.set_xlabel('Time (s)')
    axn.set_ylabel('Amplitude (V)')
    axn.grid(True)
    axn.set_title('RT EEG (Time Domain)')
  ax4.set_xlabel('Frequency (Hz)')
  ax4.set_ylabel('Intensity')
  ax4.grid(True)
  ax4.set_title('RT EEG (Freq Domain)')
  ax4.axis([0, 30, 0, 15])
  fig1.tight_layout()
  plt.draw()
  while(1):
    sampledata = data() 
    timestart = sampledata[0][0]
    timeend = sampledata[0][-1]
    for axn in [ax1, ax2, ax3]:
      axn.axis([timestart, timeend, 0, 3.5])
    l1, =  ax1.plot(sampledata[0], [3*i for i in sampledata[1]], 'r-')
    l2, = ax2.plot(sampledata[0], [3*i for i in sampledata[2]], 'b-')
    l3, = ax3.plot(sampledata[0], [3*i for i in sampledata[3]], 'g-')
    datasize = len(sampledata[0])
    timestep = sampledata[0][1] - sampledata[0][0] 
    freqfft = fft.fftfreq(len(sampledata[0]), d=timestep)
    fftdat = realfft(sampledata[2])
    fftdat[0] = 0.0
    l4, = ax4.plot(freqfft[:40], fftdat[:40], 'b--') 
    fig1.tight_layout()
    plt.draw()
    for l in [l1, l2, l3, l4]:
      l.remove()
