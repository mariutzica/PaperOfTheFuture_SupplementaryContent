# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 13:59:44 2016

@author: Maria Stoica
@description: Process the Beaver Creek precipitation data files to prepare for TopoFlow
"""

#Pandas for data frames and data manipulation
import pandas as pd
#NumPy for list data manipulation
import numpy as np
#datetime to check data availability
import datetime
#plotting functions
import matplotlib.pyplot as plt

###############################################
#                                             #
#  Clean up file containing precip rates.     #
#                                             #
###############################################

# Load file from CPEAK
ext='precipitation/'
cpeak = pd.read_csv(ext+'167_TIPBUCK_CPEAK_1993-2014.txt') #184414 data points

# Clean up : replace missing data, outliers (negative values and rates > 100 mm/hr) with -9999
#outliers: (took out -7999 and 999, but not 79.4)
#np.unique(cpeak.loc[(cpeak['value']<0)&(cpeak['value']>-9999),'value'])
#Out[58]: array([-7999.])
#cpeak.loc[cpeak['value']>100,'value']
#Out[59]:
#11805    999
#Name: value, dtype: float64
#cpeak[cpeak['cpeak_value']>70]
#Out[55]:
#             site_id        date  hour          measurement  cpeak_value unit  \
#time-seconds
#925736400      CPEAK  1999-05-03  1300  Tipping Rain Bucket         79.4   mm
#
#             flag  time-seconds
#time-seconds
#925736400       G     925736400
cpeak.loc[cpeak['flag']=='M','value']=-9999
cpeak.loc[(cpeak['value']<0)&(cpeak['value']>-9999),'value']=-9999
cpeak.loc[cpeak['value']>100,'value']=-9999
# Convert time to seconds from January 1st, 1970 at 12:00am
cpeak['time-seconds']=cpeak['date'].apply(lambda x: (datetime.datetime.strptime(x, '%Y-%m-%d')-\
    datetime.datetime(1970,1,1)).total_seconds())+cpeak['hour']*36
# Print rates to file in mm/hr and print delta_t
cpeak['value'].to_csv(ext+'CPEAK_precip_values.csv',index=False)
cpeak.index=cpeak['time-seconds']
cpeak.rename(columns={'value':'cpeak_value'}, inplace=True)
a=cpeak.head(len(cpeak)-1)['time-seconds']
b=cpeak.tail(len(cpeak)-1)['time-seconds']
a.index=range(len(a))
b.index=range(len(a))
delta_t=b-a
delta_t.to_csv(ext+'CPEAK_precip_delta_t.csv',index=False)


# Load file from CRREL
crrel = pd.read_csv(ext+'167_TIPBUCK_CRREL_2007-2014.txt') #65530 data points
crrel.loc[crrel['flag']=='M','value']=-9999
crrel['time-seconds']=crrel['date'].apply(lambda x: (datetime.datetime.strptime(x, '%Y-%m-%d')-\
    datetime.datetime(1970,1,1)).total_seconds())+crrel['hour']*36
crrel['value'].to_csv(ext+'CRREL_precip_values.csv',index=False)
crrel.index=crrel['time-seconds']
crrel.rename(columns={'value':'crrel_value'}, inplace=True)
a=crrel.head(len(crrel)-1)['time-seconds']
b=crrel.tail(len(crrel)-1)['time-seconds']
a.index=range(len(a))
b.index=range(len(a))
delta_t=b-a
delta_t.to_csv(ext+'CRREL_precip_delta_t.csv',index=False)

# Load file from CARSNOW
carsnow = pd.read_csv(ext+'167_TIPBUCK_CARSNOW_2006-2014.txt') #71810 data points
carsnow.loc[carsnow['flag']=='M','value']=-9999
carsnow['time-seconds']=carsnow['date'].apply(lambda x: (datetime.datetime.strptime(x, '%Y-%m-%d')-\
    datetime.datetime(1970,1,1)).total_seconds())+carsnow['hour']*36
carsnow['value'].to_csv(ext+'CARSNOW_precip_values.csv',index=False)
carsnow.index=carsnow['time-seconds']
carsnow.rename(columns={'value':'carsnow_value'}, inplace=True)
a=carsnow.head(len(carsnow)-1)['time-seconds']
b=carsnow.tail(len(carsnow)-1)['time-seconds']
a.index=range(len(a))
b.index=range(len(a))
delta_t=b-a
delta_t.to_csv(ext+'CARSNOW_precip_delta_t.csv',index=False)

# Load file from HR1A
hr1a = pd.read_csv(ext+'167_TIPBUCK_HR1A_2001-2014.txt') #109413 data points
hr1a.loc[hr1a['flag']=='M','value']=-9999
hr1a['time-seconds']=hr1a['date'].apply(lambda x: (datetime.datetime.strptime(x, '%Y-%m-%d')-\
    datetime.datetime(1970,1,1)).total_seconds())+hr1a['hour']*36
hr1a['value'].to_csv(ext+'HR1A_precip_values.csv',index=False)
hr1a.index=hr1a['time-seconds']
hr1a.rename(columns={'value':'hr1a_value'}, inplace=True)
a=hr1a.head(len(hr1a)-1)['time-seconds']
b=hr1a.tail(len(hr1a)-1)['time-seconds']
a.index=range(len(a))
b.index=range(len(a))
delta_t=b-a
delta_t.to_csv(ext+'HR1A_precip_delta_t.csv',index=False)

# Formatting for creating a precipitation grid from the 4 data collection points
def print_header2(f):
    f.write('%-15s %-15s %-15s %-15s %-15s\n' % ('Time','CPEAK','CRREL','CARSNOW','HR1A'))
    f.write('-'*45+'\n')
    f.write('%-15s %-15s %-15s %-15s %-15s\n' % ('X','-147.4990579','-147.4903787','-147.5606703','-147.5435743'))
    f.write('%-15s %-15s %-15s %-15s %-15s\n' % ('Y','65.19275149','65.15425986','65.15065772','65.17091866'))

#combine
temp=pd.concat([cpeak['cpeak_value'], crrel['crrel_value'], carsnow['carsnow_value'],\
    hr1a['hr1a_value']], axis=1)
temp = temp.replace(-9999,np.nan)
temp=temp.dropna(how='all')
temp = temp.replace(np.nan,-9999)
temp.index = (temp.index-temp.index[0])/3600 #convert index to hr

f = open(ext+'precipitation_hourly_rate.txt', 'w')
print_header2(f)
for row in range(len(temp)):
    f.write('%-15s %-15s %-15s %-15s %-15s\n' % (temp.index[row],temp.loc[temp.index[row],'cpeak_value']\
        ,temp.loc[temp.index[row],'crrel_value'],temp.loc[temp.index[row],'carsnow_value'],temp.loc[temp.index[row],'hr1a_value']))
f.close()

## Generate some quick plots for analysis
#plt.plot(temp.loc[temp['crrel_value']!=-9999].index/24,\
#    temp.loc[temp['crrel_value']!=-9999,'crrel_value'], 'r-')
#plt.xlabel('time (days after CPEAK start date 1993-09-21  1400)')
#plt.ylabel('precipitation (mm/hr)')
#plt.title('CRREL')
#plt.savefig(ext+'crrel_precip.png')
#plt.clf()
#
#plt.plot(temp.loc[temp['cpeak_value']!=-9999].index/24,\
#    temp.loc[temp['cpeak_value']!=-9999,'cpeak_value'], 'r-')
#plt.xlabel('time (days after CPEAK start date 1993-09-21  1400)')
#plt.ylabel('precipitation (mm/hr)')
#plt.title('CPEAK')
#plt.savefig(ext+'cpeak_precip.png')
#plt.clf()
#
#plt.plot(temp.loc[temp['hr1a_value']!=-9999].index/24,\
#    temp.loc[temp['hr1a_value']!=-9999,'hr1a_value'], 'r-')
#plt.xlabel('time (days after CPEAK start date 1993-09-21  1400)')
#plt.ylabel('precipitation (mm/hr)')
#plt.title('HR1A')
#plt.savefig(ext+'hr1a_precip.png')
#plt.clf()
#
#plt.plot(temp.loc[temp['carsnow_value']!=-9999].index/24,\
#    temp.loc[temp['carsnow_value']!=-9999,'carsnow_value'], 'r-')
#plt.xlabel('time (days after CPEAK start date 1993-09-21  1400)')
#plt.ylabel('precipitation (mm/hr)')
#plt.title('CARSNOW')
#plt.savefig(ext+'carsnow_precip.png')
