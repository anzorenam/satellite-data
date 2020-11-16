#!/usr/bin/env python3.7
# -*- coding: utf8 -*-

import matplotlib as mat
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import seaborn as sns
import astropy.io.fits as fits
import time
import datetime

sns.set(rc={"figure.figsize":(8,4)})
sns.set_context('paper',font_scale=1.5,rc={'lines.linewidth':1.5})
sns.set_style('ticks')
plt.rc('text',usetex=True)
plt.rc('text.latex',preamble=r'\usepackage[utf8]{inputenc} \usepackage[T1]{fontenc} \usepackage[spanish]{babel} \usepackage{amsmath,amsfonts,amssymb} \usepackage{siunitx}')

tstart=datetime.datetime(2017,9,6,0,0)
t0=datetime.datetime(2017,9,6,10,00)
t1=datetime.datetime(2017,9,6,20,00)
te0=datetime.datetime(2017,9,6,15,36)
te1=datetime.datetime(2017,9,6,16,36)
tmf0=datetime.datetime(2017,9,6,15,52)
tmf1=datetime.datetime(2017,9,6,12,2)

f2=fits.open('lat_spectrum_20170904.fits')
gspec=f2[1].data['COUNTS']
for j in range(0,10):
  print(f2[2].data[j])
f2.close()
print(np.shape(gspec))
tspec=[tstart+datetime.timedelta(minutes=j) for j in range(0,1440)]
fig,ax=plt.subplots(nrows=1,ncols=1,sharex=False,sharey=True)
ax.plot(tspec,np.sum(gspec[:,5:6],axis=1))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval=10))
ax.axvline(x=mdates.date2num(tmf0))
ax.axvline(x=mdates.date2num(tmf1))
ax.axvspan(te0,te1,alpha=0.2)
plt.xlabel(r'$\text{Universal time}$',x=0.9,ha='right')
plt.ylabel(r'Flux $\left(\si{\per\cm\square\per\second}\right)$')
#plt.xlim(mdates.date2num(t0),mdates.date2num(t1))
plt.tight_layout(pad=1.0)
#plt.savefig('gammas_170906.pdf')
plt.show()
