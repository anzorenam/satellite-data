#!/usr/bin/env python3.7
# -*- coding: utf8 -*-

import matplotlib as mat
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import gbm.data as gdata
import gbm.time as gtime
import gbm.binning.binned as gbin
import gbm.background as gback
import gbm.background.binned as gback_bin
import datetime

day=4
dname='2017_09_{0:02d}/glg_cspec_'.format(day)
home='/run/media/cosmicray/PHOTON/backup-210315/proyectos/scicrt'
if day==4:
  te0=datetime.datetime(2017,9,4,20,10)
  te1=datetime.datetime(2017,9,4,20,50)
  name_b0='{0}b0_bn170904855_v00.pha'.format(dname)
  name_b1='{0}b1_bn170904855_v00.pha'.format(dname)
elif day==10:
  name_b0='{0}b0_bn170910671_v01.pha'.format(dname)
  name_b1='{0}b1_bn170910671_v01.pha'.format(dname)
  te0=datetime.datetime(2017,9,10,15,40)
  te1=datetime.datetime(2017,9,10,16,20)

tbin=1.024
Nbin=16
b0=gdata.Cspec.open(name_b0)
b1=gdata.Cspec.open(name_b1)
rebin_b0=b0.rebin_time(gbin.rebin_by_time,Nbin*tbin)
rebin_b1=b1.rebin_time(gbin.rebin_by_time,Nbin*tbin)
T0=b0.trigtime
TE0,TE1=gtime.Met.from_datetime(te0),gtime.Met.from_datetime(te1)
src_range=(TE0.met-T0,TE1.met-T0)
g0=rebin_b0.slice_time(src_range)
g1=rebin_b1.slice_time(src_range)
bkgd_times=[(-1200.0,-100.0),(100.0,1130.0)]
erange=np.array([[2160.0,2240.0],[4300.0,4600.0],[5900.0,6250.0]])
gamma_high=gdata.GbmDetectorCollection.from_list([g0,g1])
poly_order=5
fig,ax=plt.subplots(nrows=1,ncols=1,sharex=False,sharey=True)
for j in range(0,3):
  ltime=gamma_high.to_lightcurve(time_range=src_range,energy_range=erange[j,:])
  backfitter=gback.BackgroundFitter.from_phaii(g0,gback_bin.Polynomial,time_ranges=bkgd_times)
  backfitter.fit(order=poly_order)
  bkgd=backfitter.interpolate_bins(g0.data.tstart,g0.data.tstop)
  lc_bkgd0=bkgd.integrate_energy(*erange[j,:])
  backfitter=gback.BackgroundFitter.from_phaii(g1,gback_bin.Polynomial,time_ranges=bkgd_times)
  backfitter.fit(order=poly_order)
  bkgd=backfitter.interpolate_bins(g0.data.tstart,g1.data.tstop)
  lc_bkgd1=bkgd.integrate_energy(*erange[j,:])
  grate=ltime[0].rates+ltime[1].rates
  bk=lc_bkgd0.rates+lc_bkgd1.rates
  time=np.array([(gtime.Met(t)).datetime for t in ltime[0].centroids+T0])
  ax.plot(time,grate,ds='steps-mid')
  ax.plot(time,bk,ds='steps-mid')
  ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
  ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval=1))
#plt.xlim(te0,te1)
#plt.xlim(1e0,1e1)
#plt.ylim(1e-2,2e0)
plt.show()
