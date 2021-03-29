#!/usr/bin/env python3.7
# -*- coding: utf8 -*-

import matplotlib.dates as mdates
import datetime
import numpy as np

day=6
xname='g15_xray_201709{0:02d}.dat'.format(day)
xfile=open(xname,'r')
xray=np.zeros([45000,2])
txray=np.zeros(45000)
j=0
for line in xfile:
  k=line.split(',')
  if len(k)==7 and k[0]!='time_tag':
    h=datetime.datetime.strptime(k[0],'%Y-%m-%d %H:%M:%S.%f')
    txray[j]=mdates.date2num(h)
    xray[j,:]=np.array([k[2],k[5]],dtype=float)
    j+=1

SEL=txray!=0
txray=txray[SEL]
sxray=xray[SEL,1]
sxray=sxray-np.amin(sxray)
sxray=sxray/np.amax(sxray)
name='sxray-1709{0:02d}.dat'.format(day)
fdat=open(name,'w')
np.savetxt(fdat,txray,newline=' ')
fdat.write('\n')
np.savetxt(fdat,sxray,newline=' ')
fdat.close()
