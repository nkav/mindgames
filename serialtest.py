import re
from numpy import fft
import numpy as np
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import gridspec
from realtime import data 

#############################
###Create plot and subplot###
#############################

fig1 = plt.figure()

ax1 = plt.subplot2grid((3,4), (0,0), colspan=2)
ax2 = plt.subplot2grid((3,4), (1,0), colspan=2, sharex=ax1)
ax3 = plt.subplot2grid((3,4), (2,0), colspan=2, sharex=ax1)
ax4 = plt.subplot2grid((3,4), (0,2), colspan=2, rowspan=2)

#####################
###Initialize Axes###
#####################

xdata  = []
y1data = []
y2data = []
y3data = []

line1, = ax1.plot(xdata, y1data, 'r-') 
line2, = ax2.plot(xdata, y2data, 'b-') 
line3, = ax3.plot(xdata, y3data, 'g-') 

for axn in [ax1, ax2, ax3]:
  axn.set_xlabel('Time (s)')
  axn.set_ylabel('Amplitude (mV)')
  axn.grid(True)
  axn.set_title('RT EEG (Time Domain)')
  axn.axis([0, 2, 0, 5000])

def update_line(num):
  t,y1, y2, y3 = sampledata[0][num], sampledata[1][num], sampledata[2][num], sampledata[3][num]
  xdata.append(t)
  y1data.append(y1)
  y2data.append(y2)
  y3data.append(y3)
  line1.set_data(xdata,y1data)
  line2.set_data(xdata,y2data)
  line3.set_data(xdata,y3data)
  #xmin, xmax = ax.get_xlim()
  #if t >= xmax:
  #    ax.set_xlim(xmin, 2*xmax)
  #    ax.figure.canvas.draw()
  return [line1, line2, line3] 


def realfft(sampledata):
  return np.absolute(fft.rfft(sampledata))

if __name__ == '__main__':
  sampledata = data(105) 
  datasize = len(sampledata[0])
  line1_ani = animation.FuncAnimation(fig1, update_line, 100, 
      interval=50, blit=True, repeat=False) 

  timestep = sampledata[0][1] - sampledata[0][0] 
  freqfft = fft.fftfreq(len(sampledata[0]), d=timestep)

  fft1 = realfft(sampledata[1])
  fft2 = realfft(sampledata[2])
  fft3 = realfft(sampledata[3])

  ax4.set_xlabel('Frequency (Hz)')
  ax4.set_ylabel('Intensity')
  ax4.grid(True)
  ax4.set_title('RT EEG (Freq Domain)')
  ax4.axis([0, 20, 0, 86532])
  fft2[0] = 0.0
  ax4.plot(freqfft[:50], fft2[:50], 'r--') 
  fig1.tight_layout()
  plt.show()
