#!/usr/bin/env python3.7
# -*- coding: utf8 -*-

import matplotlib.dates as mdates
import numpy as np
import gbm.data as gdata
import gbm.time as gtime
import gbm.binning.binned as gbin
import datetime

day=6
if day==4:
  tstart=datetime.datetime(2017,9,4,0,0)
  te0=datetime.datetime(2017,9,4,17,30)
  te1=datetime.datetime(2017,9,4,23,30)
  tmf0=datetime.datetime(2017,9,4,20,32)
elif day==5:
  tstart=datetime.datetime(2017,9,5,0,0)
  te0=datetime.datetime(2017,9,5,14,30)
  te1=datetime.datetime(2017,9,5,20,30)
  tmf0=datetime.datetime(2017,9,5,17,42)
elif day==6:
  tstart=datetime.datetime(2017,9,6,0,0)
  te0=datetime.datetime(2017,9,6,12,50)
  te1=datetime.datetime(2017,9,6,18,50)
  tmf0=datetime.datetime(2017,9,6,15,52)

dname='2017_09_0{0}/glg_cspec_'.format(day)
home='/run/media/cosmicray/PHOTON/backup-210315/proyectos/scicrt'
tbin=32.762
nuclear=False
b0=gdata.Cspec.open('{0}b0_17090{1}_v00.pha'.format(dname,day))
b1=gdata.Cspec.open('{0}b1_17090{1}_v00.pha'.format(dname,day))
n1=gdata.Cspec.open('{0}n1_17090{1}_v00.pha'.format(dname,day))
n3=gdata.Cspec.open('{0}n3_17090{1}_v00.pha'.format(dname,day))
n5=gdata.Cspec.open('{0}n5_17090{1}_v00.pha'.format(dname,day))
n9=gdata.Cspec.open('{0}n9_17090{1}_v00.pha'.format(dname,day))
na=gdata.Cspec.open('{0}na_17090{1}_v00.pha'.format(dname,day))
nb=gdata.Cspec.open('{0}nb_17090{1}_v00.pha'.format(dname,day))

T0,T1,Tm=gtime.Met.from_datetime(te0),gtime.Met.from_datetime(te1),gtime.Met.from_datetime(tmf0)
src_range=(T0.met,T1.met)

rebin_n1=n1.rebin_time(gbin.rebin_by_time,tbin)
rebin_n3=n3.rebin_time(gbin.rebin_by_time,tbin)
rebin_n5=n5.rebin_time(gbin.rebin_by_time,tbin)
rebin_n9=n9.rebin_time(gbin.rebin_by_time,tbin)
rebin_na=na.rebin_time(gbin.rebin_by_time,tbin)
rebin_nb=nb.rebin_time(gbin.rebin_by_time,tbin)
rebin_b0=b0.rebin_time(gbin.rebin_by_time,tbin)
rebin_b1=b1.rebin_time(gbin.rebin_by_time,tbin)

gamma_sun=gdata.GbmDetectorCollection.from_list([rebin_n1,rebin_n3,rebin_n5])
gamma_asn=gdata.GbmDetectorCollection.from_list([rebin_n9,rebin_na,rebin_nb])
gamma_high=gdata.GbmDetectorCollection.from_list([rebin_b0,rebin_b1])
lgsun=gamma_sun.to_lightcurve(time_range=src_range,energy_range=(50.0,300.0))
lgasn=gamma_asn.to_lightcurve(time_range=src_range,energy_range=(50.0,300.0))
lhigh=gamma_high.to_lightcurve(time_range=src_range,energy_range=(2000.0,6000.0))

if nuclear==False:
  gamma=(lgsun[0].rates+lgsun[1].rates+lgsun[2].rates)-(lgasn[0].rates+lgasn[1].rates+lgasn[2].rates)
  times=np.array([(gtime.Met(t)).datetime for t in lgsun[0].centroids])
  name='{0}/data-analysis/event/gamma-event/hxray-1709{1:02d}.dat'.format(home,day)
else:
  gamma=lhigh[0].rates-lhigh[1].rates
  times=np.array([(gtime.Met(t)).datetime for t in lhigh[0].centroids])
  name='{0}/data-analysis/event/gamma-event/ngray-17090{1:02d}.dat'.format(home,day)

times=mdates.date2num(times)
gamma=gamma-np.amin(gamma)
gamma=gamma/np.amax(gamma)
fdat=open(name,'w')
np.savetxt(fdat,times,newline=' ')
fdat.write('\n')
np.savetxt(fdat,gamma,newline=' ')
fdat.close()
