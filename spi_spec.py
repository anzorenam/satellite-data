#!/usr/bin/env python3.7
# -*- coding: utf8 -*-

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

rev_num='1858'
sname='scw/{0}/spi_oper.fits'.format(rev_num)
tjd=datetime.datetime(1999,12,31,23,58,55,816)
f=fits.open(sname)
dts=f[1].data['TIME']
N=np.size(dts)
erange=np.array([[2.16,2.24],[4.30,4.50],[6.0,6.2]])
ecounts=(1.0/1000.0)*(f[1].data['ENERGY'])
tfits=[tjd+datetime.timedelta(days=d) for d in dts]
t0,t1=tfits[0],tfits[-1]
print(t0,t1)
t_lap=np.rint((t1-t0).total_seconds())
Nseg=60
tbins=np.arange(0,t_lap,Nseg)
Mbins=np.shape(tbins)[0]
tcounts=[tfits[0]+datetime.timedelta(seconds=j) for j in tbins]
tdiff=np.zeros(N)
for j in range(0,N):
  tdiff[j]=(tfits[j]-t0).total_seconds()
tdig=np.digitize(tdiff,bins=tbins)

fig,ax=plt.subplots(nrows=1,ncols=1,sharex=False,sharey=True)
for ksel in range(0,3):
  ncapture=1.0*np.logical_and(ecounts>=erange[ksel,0],ecounts<=erange[ksel,1])
  prod=ncapture*tdig
  ncounts,b=np.histogram(prod[prod!=0],bins=Mbins)
  m,dstd=np.mean(ncounts[0:25]),np.std(ncounts[0:25])
  ax.plot(tcounts,(ncounts-m)/dstd,ds='steps-mid')
ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval=1))
plt.xlabel(r'Tiempo universal $\left[\text{2017-Sep-04}\right]$',x=0.95,ha='right')
plt.ylabel(r'Cuentas $\left[\si{\per\minute}\right]$')
ebins=np.arange(1,10,0.04)
Kbins=np.shape(ebins)[0]
espec=np.zeros([Kbins,Mbins+1])
ebkg=np.zeros([Kbins,Mbins+1])
edig=np.digitize(ecounts,bins=ebins)
for es,ts in zip(edig,tdig):
  if ts>=28 and ts<=32:
    espec[es,ts]+=1.0
  elif ts>=0 and ts<=25:
    ebkg[es,ts]+=1.0

gamma=np.sum(espec,axis=1)/np.sum(espec)
gbkg=np.sum(ebkg,axis=1)/np.sum(ebkg)
fig,ax=plt.subplots(nrows=1,ncols=1,sharex=False,sharey=True)
ax.loglog(ebins,gamma,ds='steps-mid')
ax.loglog(ebins,gbkg,ds='steps-mid')
plt.show()
