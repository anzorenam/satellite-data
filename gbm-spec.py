#!/usr/bin/env python3.7
# -*- coding: utf8 -*-

import matplotlib as mat
import matplotlib.pyplot as plt
import gbm.data as gdata
import gbm.time as gtime
import astropy.io.fits as fits

import time
import datetime
import seaborn as sns

sns.set(rc={"figure.figsize":(8,4)})
sns.set_context('paper',font_scale=1.5,rc={'lines.linewidth':1.5})
sns.set_style('ticks')
plt.rc('text',usetex=True)
plt.rc('text.latex',preamble=r'\usepackage[utf8]{inputenc} \usepackage[T1]{fontenc} \usepackage[spanish]{babel} \usepackage{amsmath,amsfonts,amssymb} \usepackage{siunitx}')

tstart=datetime.datetime(2017,9,6,0,0)
t0=datetime.datetime(2017,9,6,11,00)
t1=datetime.datetime(2017,9,6,16,00)
te0=datetime.datetime(2017,9,6,15,36)
te1=datetime.datetime(2017,9,6,16,36)
tmf0=datetime.datetime(2017,9,6,15,52)
tmf1=datetime.datetime(2017,9,6,12,2)

b0=gdata.Cspec.open('2017_09_06/glg_cspec_b0_170906_v00.pha')
b1=gdata.Cspec.open('2017_09_06/glg_cspec_b1_170906_v00.pha')
n0=gdata.Cspec.open('2017_09_06/glg_cspec_n0_170906_v00.pha')
n1=gdata.Cspec.open('2017_09_06/glg_cspec_n1_170906_v00.pha')
n2=gdata.Cspec.open('2017_09_06/glg_cspec_n2_170906_v00.pha')
n3=gdata.Cspec.open('2017_09_06/glg_cspec_n3_170906_v00.pha')
n4=gdata.Cspec.open('2017_09_06/glg_cspec_n4_170906_v00.pha')
n5=gdata.Cspec.open('2017_09_06/glg_cspec_n5_170906_v00.pha')
n6=gdata.Cspec.open('2017_09_06/glg_cspec_n6_170906_v00.pha')
n7=gdata.Cspec.open('2017_09_06/glg_cspec_n7_170906_v00.pha')
n8=gdata.Cspec.open('2017_09_06/glg_cspec_n8_170906_v00.pha')
n9=gdata.Cspec.open('2017_09_06/glg_cspec_n9_170906_v00.pha')
na=gdata.Cspec.open('2017_09_06/glg_cspec_na_170906_v00.pha')
nb=gdata.Cspec.open('2017_09_06/glg_cspec_nb_170906_v00.pha')
gamma_sun=gdata.GbmDetectorCollection.from_list([n0,n1,n3])
gamma_asn=gdata.GbmDetectorCollection.from_list([n6,n7,n9])
T0,T1,Tm=gtime.Met.from_datetime(t0),gtime.Met.from_datetime(t1),gtime.Met.from_datetime(tmf1)
src_range=(T0.met,T1.met)

gspecs=gamma_sun.to_spectrum(time_range=src_range)
gapecs=gamma_asn.to_spectrum(time_range=src_range)
ltimes=gamma_asn.to_lightcurve(time_range=src_range)
fig,ax=plt.subplots(nrows=1,ncols=1,sharex=False,sharey=False)
for ltime in ltimes:
  ax.plot(ltime.centroids,ltime.rates,ds='steps-mid')
ax.axvline(x=Tm.met)
sun_spec=gspecs[0].rates+gspecs[1].rates+gspecs[2].rates
asn_spec=gapecs[0].rates+gapecs[1].rates+gapecs[2].rates
fig,ax=plt.subplots(nrows=1,ncols=1,sharex=False,sharey=False)
ax.loglog((1.0/1000.0)*gspecs[0].centroids,sun_spec,ds='steps-mid')
ax.loglog((1.0/1000.0)*gspecs[0].centroids,asn_spec,ds='steps-mid')
plt.xlabel(r'Energy $\left(\si{\mega\electronvolt}\right)$',x=0.9,ha='right')
plt.ylabel(r'$\log_{10}\left(\si{Counts}\right)$')
plt.tight_layout(pad=1.0)
#plt.savefig('gammas_low_170906.pdf')
plt.show()
