#!/usr/bin/env python3.7
# -*- coding: utf8 -*-

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import datetime
import argparse
import numpy as np
import os

sns.set(rc={"figure.figsize":(8,4)})
sns.set_context('paper',font_scale=1.5,rc={'lines.linewidth':1.5})
sns.set_style('ticks')
plt.rc('text',usetex=True)
plt.rc('text.latex',preamble=r'\usepackage[utf8]{inputenc} \usepackage[T1]{fontenc} \usepackage[spanish]{babel} \usepackage{amsmath,amsfonts,amssymb} \usepackage{siunitx}')

home=os.environ['HOME']
tstart=datetime.datetime(2017,9,6,9)
t0=mdates.date2num(datetime.datetime(2017,9,6,10))
t1=mdates.date2num(datetime.datetime(2017,9,6,20))
te0=datetime.datetime(2017,9,6,15,36)
te1=datetime.datetime(2017,9,6,16,36)
tmf0=datetime.datetime(2017,9,6,15,51)
tmf1=datetime.datetime(2017,9,6,12,2)


fdir='{0}/proyectos/scicrt/data-analysis'.format(home)
xray=np.loadtxt('{0}/xray-170906.dat'.format(fdir),dtype=np.float)
M=60*15
txray=[tstart+datetime.timedelta(minutes=j) for j in range(0,M)]
c0=sns.cubehelix_palette(8,start=2,rot=0,dark=0.1,light=.95,reverse=True)[0]

fig,ax=plt.subplots(nrows=1,ncols=1,sharex=False,sharey=True)
ax.semilogy(txray,xray)
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval=10))
ax.axvline(x=mdates.date2num(tmf0))
ax.axvline(x=mdates.date2num(tmf1))
ax.axvspan(te0,te1,alpha=0.2)
plt.xlabel(r'$\text{Universal time}$',x=0.9,ha='right')
plt.ylabel(r'GOES Xray flux $\left[\si{\watt\per\square\metre}\right]$')
plt.xlim(t0,t1)
plt.tight_layout(pad=1.0)
plt.show()
#plt.savefig('goesx_170906.pdf')
