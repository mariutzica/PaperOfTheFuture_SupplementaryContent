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

# Extract the time period for the desired event
time_min=(datetime.datetime.strptime('2008/07/28  16:00:00',\
    '%Y/%m/%d %H:%M:%S')-datetime.datetime(1970,1,1)).total_seconds()
time_max=(datetime.datetime.strptime('2008/07/30  18:00:00',\
    '%Y/%m/%d %H:%M:%S')-datetime.datetime(1970,1,1)).total_seconds()
cpeak=cpeak[(cpeak['time-seconds']>=time_min)&(cpeak['time-seconds']<=time_max)]

# Print rates to file in mm/hr and print delta_t
cpeak['value'].to_csv(ext+'CPEAK_precip_values.csv',index=False)
#subsampled precip file 1800 repetitions for each value
np.repeat(cpeak['value'],1800)\
         .to_csv(ext+'CPEAK_precip_values_2s.csv',index=False)
cpeak.index=cpeak['time-seconds']
cpeak.rename(columns={'value':'cpeak_value'}, inplace=True)
a=cpeak.head(len(cpeak)-1)['time-seconds']
b=cpeak.tail(len(cpeak)-1)['time-seconds']
a.index=range(len(a))
b.index=range(len(a))
delta_t=b-a
delta_t.to_csv(ext+'CPEAK_precip_delta_t.csv',index=False)



# Load file from CRREL
#crrel = pd.read_csv(ext+'167_TIPBUCK_CRREL_2007-2014.txt') #65530 data points
#crrel.loc[crrel['flag']=='M','value']=-9999
#crrel['time-seconds']=crrel['date'].apply(lambda x: (datetime.datetime.strptime(x, '%Y-%m-%d')-\
#    datetime.datetime(1970,1,1)).total_seconds())+crrel['hour']*36
#crrel['value'].to_csv(ext+'CRREL_precip_values.csv',index=False)
#crrel.index=crrel['time-seconds']
#crrel.rename(columns={'value':'crrel_value'}, inplace=True)
#a=crrel.head(len(crrel)-1)['time-seconds']
#b=crrel.tail(len(crrel)-1)['time-seconds']
#a.index=range(len(a))
#b.index=range(len(a))
#delta_t=b-a
#delta_t.to_csv(ext+'CRREL_precip_delta_t.csv',index=False)
#
## Load file from CARSNOW
#carsnow = pd.read_csv(ext+'167_TIPBUCK_CARSNOW_2006-2014.txt') #71810 data points
#carsnow.loc[carsnow['flag']=='M','value']=-9999
#carsnow['time-seconds']=carsnow['date'].apply(lambda x: (datetime.datetime.strptime(x, '%Y-%m-%d')-\
#    datetime.datetime(1970,1,1)).total_seconds())+carsnow['hour']*36
#carsnow['value'].to_csv(ext+'CARSNOW_precip_values.csv',index=False)
#carsnow.index=carsnow['time-seconds']
#carsnow.rename(columns={'value':'carsnow_value'}, inplace=True)
#a=carsnow.head(len(carsnow)-1)['time-seconds']
#b=carsnow.tail(len(carsnow)-1)['time-seconds']
#a.index=range(len(a))
#b.index=range(len(a))
#delta_t=b-a
#delta_t.to_csv(ext+'CARSNOW_precip_delta_t.csv',index=False)
#
## Load file from HR1A
#hr1a = pd.read_csv(ext+'167_TIPBUCK_HR1A_2001-2014.txt') #109413 data points
#hr1a.loc[hr1a['flag']=='M','value']=-9999
#hr1a['time-seconds']=hr1a['date'].apply(lambda x: (datetime.datetime.strptime(x, '%Y-%m-%d')-\
#    datetime.datetime(1970,1,1)).total_seconds())+hr1a['hour']*36
#hr1a['value'].to_csv(ext+'HR1A_precip_values.csv',index=False)
#hr1a.index=hr1a['time-seconds']
#hr1a.rename(columns={'value':'hr1a_value'}, inplace=True)
#a=hr1a.head(len(hr1a)-1)['time-seconds']
#b=hr1a.tail(len(hr1a)-1)['time-seconds']
#a.index=range(len(a))
#b.index=range(len(a))
#delta_t=b-a
#delta_t.to_csv(ext+'HR1A_precip_delta_t.csv',index=False)
#
## Formatting for creating a precipitation grid from the 4 data collection points
#def print_header2(f):
#    f.write('%-15s %-15s %-15s %-15s %-15s\n' % ('Time','CPEAK','CRREL','CARSNOW','HR1A'))
#    f.write('-'*45+'\n')
#    f.write('%-15s %-15s %-15s %-15s %-15s\n' % ('X','-147.4990579','-147.4903787','-147.5606703','-147.5435743'))
#    f.write('%-15s %-15s %-15s %-15s %-15s\n' % ('Y','65.19275149','65.15425986','65.15065772','65.17091866'))
#
##combine
#temp=pd.concat([cpeak['cpeak_value'], crrel['crrel_value'], carsnow['carsnow_value'],\
#    hr1a['hr1a_value']], axis=1)
#temp = temp.replace(-9999,np.nan)
#temp=temp.dropna(how='all')
#temp = temp.replace(np.nan,-9999)
#temp.index = (temp.index-temp.index[0])/3600 #convert index to hr
#
#f = open(ext+'precipitation_hourly_rate.txt', 'w')
#print_header2(f)
#for row in range(len(temp)):
#    f.write('%-15s %-15s %-15s %-15s %-15s\n' % (temp.index[row],temp.loc[temp.index[row],'cpeak_value']\
#        ,temp.loc[temp.index[row],'crrel_value'],temp.loc[temp.index[row],'carsnow_value'],temp.loc[temp.index[row],'hr1a_value']))
#f.close()
#
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


#relative humidity data
#ext='relative humidity/'
#cpeak = pd.read_csv(ext+'303_RH_CPEAK_1993-2014.txt') #553242 data points
#cpeak.loc[cpeak['mean_flag']=='M','relhum']=-9999
##take out 7999s -- why are some negative and some positive?
#cpeak.loc[abs(cpeak['relhum'])==7999,'relhum']=-9999
#cpeak['time-seconds']=cpeak['date'].apply(lambda x: (datetime.datetime.strptime(x, '%Y-%m-%d')-\
#    datetime.datetime(1970,1,1)).total_seconds())+cpeak['hour']*36
#cpeak['relhum'].to_csv(ext+'CPEAK_relhum_values.csv',index=False)
#cpeak.index=cpeak['time-seconds']
#cpeak.rename(columns={'relhum':'cpeak_relhum'}, inplace=True)
#a=cpeak.head(len(cpeak)-1)['time-seconds']
#b=cpeak.tail(len(cpeak)-1)['time-seconds']
#a.index=range(len(a))
#b.index=range(len(a))
#delta_t=b-a
#delta_t.to_csv(ext+'CPEAK_relhum_delta_t.csv',index=False)
#
#crrel = pd.read_csv(ext+'303_RH_CRREL_1992-2014.txt') #746052 data points
#crrel.loc[crrel['mean_flag']=='M','relhum']=-9999
#crrel['time-seconds']=crrel['date'].apply(lambda x: (datetime.datetime.strptime(x, '%Y-%m-%d')-\
#    datetime.datetime(1970,1,1)).total_seconds())+crrel['hour']*36
#crrel['relhum'].to_csv(ext+'CRREL_relhum_values.csv',index=False)
#crrel.index=crrel['time-seconds']
#crrel.rename(columns={'relhum':'crrel_relhum'}, inplace=True)
#a=crrel.head(len(crrel)-1)['time-seconds']
#b=crrel.tail(len(crrel)-1)['time-seconds']
#a.index=range(len(a))
#b.index=range(len(a))
#delta_t=b-a
#delta_t.to_csv(ext+'CRREL_relhum_delta_t.csv',index=False)
#
#carsnow = pd.read_csv(ext+'303_RH_CARSNOW_2006-2014.txt') #71810 data points
#carsnow.loc[carsnow['mean_flag']=='M','relhum']=-9999
#carsnow['time-seconds']=carsnow['date'].apply(lambda x: (datetime.datetime.strptime(x, '%Y-%m-%d')-\
#    datetime.datetime(1970,1,1)).total_seconds())+carsnow['hour']*36
#carsnow['relhum'].to_csv(ext+'CARSNOW_relhum_values.csv',index=False)
#carsnow.index=carsnow['time-seconds']
#carsnow.rename(columns={'relhum':'carsnow_relhum'}, inplace=True)
#a=carsnow.head(len(carsnow)-1)['time-seconds']
#b=carsnow.tail(len(carsnow)-1)['time-seconds']
#a.index=range(len(a))
#b.index=range(len(a))
#delta_t=b-a
#delta_t.to_csv(ext+'CARSNOW_relhum_delta_t.csv',index=False)
#
#hr1a = pd.read_csv(ext+'303_RH_HR1A_2001-2014.txt') #109413 data points
#hr1a.loc[hr1a['mean_flag']=='M','relhum']=-9999
#hr1a['time-seconds']=hr1a['date'].apply(lambda x: (datetime.datetime.strptime(x, '%Y-%m-%d')-\
#    datetime.datetime(1970,1,1)).total_seconds())+hr1a['hour']*36
#hr1a['relhum'].to_csv(ext+'HR1A_relhum_values.csv',index=False)
#hr1a.index=hr1a['time-seconds']
#hr1a.rename(columns={'relhum':'hr1a_relhum'}, inplace=True)
#a=hr1a.head(len(hr1a)-1)['time-seconds']
#b=hr1a.tail(len(hr1a)-1)['time-seconds']
#a.index=range(len(a))
#b.index=range(len(a))
#delta_t=b-a
#delta_t.to_csv(ext+'HR1A_relhum_delta_t.csv',index=False)
#
##combine
##need to average multiple data points
#hr1a_av = pd.DataFrame(index=np.unique(hr1a['time-seconds']),columns=['hr1a_relhum'])
#for i in hr1a_av.index:
#    hr1a_av.loc[i,'hr1a_relhum']=hr1a.loc[(hr1a.index==i)&(hr1a['hr1a_relhum']!=-9999),'hr1a_relhum'].mean()
#carsnow_av = pd.DataFrame(index=np.unique(carsnow['time-seconds']),columns=['carsnow_relhum'])
#for i in carsnow_av.index:
#    carsnow_av.loc[i,'carsnow_relhum']=carsnow.loc[(carsnow.index==i)&(carsnow['carsnow_relhum']!=-9999),'carsnow_relhum'].mean()
#cpeak_av = pd.DataFrame(index=np.unique(cpeak['time-seconds']),columns=['cpeak_relhum'])
#for i in cpeak_av.index:
#    cpeak_av.loc[i,'cpeak_relhum']=cpeak.loc[(cpeak.index==i)&(cpeak['cpeak_relhum']!=-9999),'cpeak_relhum'].mean()
#crrel_av = pd.DataFrame(index=np.unique(crrel['time-seconds']),columns=['crrel_relhum'])
#for i in crrel_av.index:
#    crrel_av.loc[i,'crrel_relhum']=crrel.loc[(crrel.index==i)&(crrel['crrel_relhum']!=-9999),'crrel_relhum'].mean()
#
#temp=pd.concat([cpeak_av, crrel_av, carsnow_av, hr1a_av], axis=1)
#temp = temp.replace(-9999,np.nan)
#temp=temp.dropna(how='all')
#temp = temp.replace(np.nan,-9999)
##change time to hours
#temp.index = (temp.index-temp.index[0])/3600
#
#f = open(ext+'relative_humidity.txt', 'w')
#print_header2(f)
#for row in range(len(temp)):
#    f.write('%-15s %-15s %-15s %-15s %-15s\n' % (temp.index[row],temp.loc[temp.index[row],'cpeak_relhum']\
#        ,temp.loc[temp.index[row],'crrel_relhum'],temp.loc[temp.index[row],'carsnow_relhum'],temp.loc[temp.index[row],'hr1a_relhum']))
#f.close()
#
#plt.plot(temp.loc[temp['crrel_relhum']!=-9999].index/24,\
#    temp.loc[temp['crrel_relhum']!=-9999,'crrel_relhum'], 'r-')
#plt.xlabel('time (days after CRREL start date 1992-06-12  1400)')
#plt.ylabel('relative humidity (%)')
#plt.title('CRREL')
#plt.savefig(ext+'crrel_relhum.png')
#plt.clf()
#
#plt.plot(temp.loc[temp['cpeak_relhum']!=-9999].index/24,\
#    temp.loc[temp['cpeak_relhum']!=-9999,'cpeak_relhum'], 'r-')
#plt.xlabel('time (days after CRREL start date 1992-06-12  1400)')
#plt.ylabel('relative humidity (%)')
#plt.title('CPEAK')
#plt.savefig(ext+'cpeak_relhum.png')
#plt.clf()
#
#plt.plot(temp.loc[temp['hr1a_relhum']!=-9999].index/24,\
#    temp.loc[temp['hr1a_relhum']!=-9999,'hr1a_relhum'], 'r-')
#plt.xlabel('time (days after CRREL start date 1992-06-12  1400)')
#plt.ylabel('relative humidity (%)')
#plt.title('HR1A')
#plt.savefig(ext+'hr1a_relhum.png')
#plt.clf()
#
#plt.plot(temp.loc[temp['carsnow_relhum']!=-9999].index/24,\
#    temp.loc[temp['carsnow_relhum']!=-9999,'carsnow_relhum'], 'r-')
#plt.xlabel('time (days after CRREL start date 1992-06-12  1400)')
#plt.ylabel('relative humidity (%)')
#plt.title('CARSNOW')
#plt.savefig(ext+'carsnow_relhum.png')