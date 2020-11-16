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

rev_num='1025'
sname='scw/{0}/spi_oper.fits'.format(rev_num)
tjd=datetime.datetime(1999,12,31,23,58,55,816)
f=fits.open(sname)
dts=f[1].data['TIME']
N=np.size(dts)
ecounts=(1.0/1000.0)*(f[1].data['ENERGY'])
ncapture=1.0*np.logical_and(ecounts>=0.025,ecounts<=0.05)
tfits=[tjd+datetime.timedelta(days=d) for d in dts]
t0,t1=tfits[0],tfits[-1]
print(t0,t1)
t_lap=np.rint((t1-t0).total_seconds())
Nbins=32
tbins=np.arange(0,t_lap,Nbins)
tdiff=np.zeros(N)
for j in range(0,N):
  tdiff[j]=(tfits[j]-t0).total_seconds()
tdig=np.digitize(tdiff,bins=tbins)
prod=ncapture*tdig
fig,ax=plt.subplots(nrows=1,ncols=1,sharex=False,sharey=True)
ax.hist(prod[prod!=0],bins=np.int(t_lap/Nbins),histtype='step')
plt.show()
