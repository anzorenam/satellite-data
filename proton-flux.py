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

t0=datetime.datetime(2017,9,6,10,00)
t1=datetime.datetime(2017,9,6,22,00)
tmf=datetime.datetime(2017,9,6,15,52)

jevt=0
f=open('g15_protons_20170906.dat','r')
N=3000
Nhead=283
p=np.zeros(N)
time=np.zeros(N)
for line in f:
  if jevt>=Nhead:
    k=line.split(',')
    h=datetime.datetime.strptime(k[0][:-4],'%Y-%m-%d %H:%M:%S')
    time[jevt]=mdates.date2num(h)
    p[jevt]=float(k[11])+float(k[14])+float(k[17])
  jevt+=1

# para el 06/09/17 11,14,17
# para el 04/09/17 2,5,8
mean=32
K=np.shape(np.arange(Nhead,jevt,mean))[0]
time=time[Nhead:jevt:mean]
protons=0
for j in range(0,mean):
  M=np.shape(p[j+Nhead:jevt:mean])[0]
  if M<K:
    a=np.pad(p[j+Nhead:jevt:mean],(0,K-M),'constant',constant_values=0)
  else:
    a=p[j+Nhead:jevt:mean]
  protons+=a

fig,ax=plt.subplots(nrows=1,ncols=1,sharex=False,sharey=True)
ax.plot(time,np.log10(protons),label='$>\SI{60}{\mega\electronvolt}$')
ax.axvline(x=tmf,ls=':')
plt.xlabel(r'Tiempo universal $\left[\text{2017-Sep-06}\right]$',x=0.9,ha='right')
plt.ylabel(r'$\log_{10}\left(\si{Cuentas\per\minute}\right)$')
ax.xaxis.set_major_locator(mdates.HourLocator(interval=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval=30))
plt.xlim(t0,t1)
plt.ylim(1.6,2.0)
plt.legend()
plt.tight_layout(pad=1.0)
plt.savefig('protons_170906.pdf')
plt.show()
