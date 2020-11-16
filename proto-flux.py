#!/usr/bin/env python3.7
# -*- coding: utf8 -*-

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np
import time
import datetime

sns.set(rc={"figure.figsize":(8,4)})
sns.set_context('paper',font_scale=1.5,rc={'lines.linewidth':1.5})
sns.set_style('ticks')
plt.rc('text',usetex=True)
plt.rc('text.latex',preamble=r'\usepackage[utf8]{inputenc} \usepackage[T1]{fontenc} \usepackage[spanish]{babel} \usepackage{amsmath,amsfonts,amssymb} \usepackage{siunitx}')

t0=datetime.datetime(2017,9,6,10,00)
t1=datetime.datetime(2017,9,6,20,00)
te0=datetime.datetime(2017,9,6,15,36)
te1=datetime.datetime(2017,9,6,16,36)
tmf0=datetime.datetime(2017,9,6,15,51)
tmf1=datetime.datetime(2017,9,6,12,2)

j=0
f=open('g15_protons_20170906.csv','r')
N=2919
p=np.zeros(N)
time=np.zeros(N)
for line in f:
  if j>=283:
    k=line.split(',')
    h=datetime.datetime.strptime(k[0][:-4],'%Y-%m-%d %H:%M:%S')
    time[j]=mdates.date2num(h)
    p[j]=np.float(k[11])+np.float(k[14])+np.float(k[17])
  j+=1
time=time[283:]
protons=p[283:]
fig,ax=plt.subplots(nrows=1,ncols=1,sharex=False,sharey=True)
ax.step(time,protons)
ax.axvline(x=mdates.date2num(tmf0))
ax.axvline(x=mdates.date2num(tmf1))
ax.axvspan(te0,te1,alpha=0.2)
plt.xlabel(r'$\text{Universal time}$',x=0.9,ha='right')
plt.ylabel(r'$\log_{10}\left(\si{Counts\per\second}\right)$')
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval=10))
plt.xlim(mdates.date2num(t0),mdates.date2num(t1))
plt.tight_layout(pad=1.0)
plt.savefig('protons_170906.pdf')
#plt.show()
