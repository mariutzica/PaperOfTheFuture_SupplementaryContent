# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 13:59:44 2016

@author: Maria Stoica
@description: Process the Beaver Creek discharge files and output dt and discharge files
of a selected time frame of data.
"""

#Pandas for data frames and data manipulation
import pandas as pd
#datetime to check data availability
import datetime
#plotting functions
import matplotlib.pyplot as plt

###############################################
#                                             #
#  Clean up file containing discharges.       #
#                                             #
###############################################

# Load file
ext='discharges/'
flow_data = pd.read_csv(ext+'cpcrw_flow_1969-2015.txt')

# Check data -- run these commands to determine number of discharge data collection
# sources, units for the discharge values reported, and whether or not data is reported
# as 'Good'
#np.unique(flow_data['Watershed'])
##Out[30]: array(['C2', 'C3', 'C4'], dtype=object)
#np.unique(flow_data['Units'])
##Out[32]: array(['L/s'], dtype=object)
#np.unique(flow_data['Flag'])
##Out[33]: array(['G'], dtype=object) <-- All data is good!

# Correct formatting of 'Date-Time' column so it is consistent, sort, and convert to a total
# time in seconds, with t0 = January 1, 1970 @ 12:00am (ref time in Python datetime)
flow_data.loc[:,'Date-Time']=flow_data.loc[:,'Date-Time'].str.split('/')\
    .str[2].str.split(' ').str[0]+'/'+flow_data.loc[:,'Date-Time']\
    .str.split(' ').str[0].str[:-5]+' '+flow_data.loc[:,'Date-Time']\
    .str.split(' ').str[1]
flow_data.loc[:,'Date-Time']=flow_data.loc[:,'Date-Time'].str.replace('/1/','/01/')\
    .str.replace('/1 ','/01 ')\
    .str.replace('/2/','/02/').str.replace('/2 ','/02 ')\
    .str.replace('/3/','/03/').str.replace('/3 ','/03 ').str.replace('/4','/04')\
    .str.replace('/5','/05').str.replace('/6','/06').str.replace('/7','/07')\
    .str.replace('/8','/08').str.replace('/9','/09').str.replace(' 0:',' 00:')\
    .str.replace(' 1:',' 01:').str.replace(' 2:',' 02:').str.replace(' 3:',' 03:')\
    .str.replace(' 4:',' 04:').str.replace(' 5:',' 05:').str.replace(' 6:',' 06:')\
    .str.replace(' 7:',' 07:').str.replace(' 8:',' 08:').str.replace(' 9:',' 09:')
flow_data = flow_data.sort_values('Date-Time')
flow_data['time-seconds']=flow_data['Date-Time'].apply(lambda x: (datetime.datetime.strptime(x,\
    '%Y/%m/%d %H:%M:%S')-datetime.datetime(1970,1,1)).total_seconds())

# Extract the time period for the desired event
time_min=(datetime.datetime.strptime('2008/07/28  16:00:00',\
    '%Y/%m/%d %H:%M:%S')-datetime.datetime(1970,1,1)).total_seconds()
time_max=(datetime.datetime.strptime('2008/07/30  18:00:00',\
    '%Y/%m/%d %H:%M:%S')-datetime.datetime(1970,1,1)).total_seconds()
flow_data=flow_data[(flow_data['time-seconds']>=time_min)&(flow_data['time-seconds']<=time_max)]

def create_topoflow_input_flow_files(flow_data,ext,watershed='C2'):
    # Extract the data for the C2 watershed
    temp=flow_data[flow_data['Watershed']==watershed]

    # Calculate and print delta_t between data points for the entire range
    a=temp.head(len(temp)-1)['time-seconds']
    b=temp.tail(len(temp)-1)['time-seconds']
    a.index=range(len(a))
    b.index=range(len(a))
    delta_t=b-a
    delta_t.to_csv(ext+watershed+'_flow_rate_delta_t_2008.csv',index=False)

    # Print corresponding discharge data to file, converting from L/s --> m3/s
    (temp['Flow']*.001).to_csv(ext+watershed+'_flow_rate_2008.csv',index=False)

def plot_flow_data(flow_data,ext,watershed='C2'):
    # Extract the data for the C2 watershed
    temp=flow_data[flow_data['Watershed']==watershed]
    
    # Simple plot to check the data
    plt.plot(temp['time-seconds']/3600/24-min(flow_data['time-seconds'])/3600/24,\
        temp['Flow']*.001, 'r-')
    plt.xlabel('time (days after start date 2008/07/28 16:00:00)')
    plt.ylabel('discharge rate (m$^3$/s)')
    plt.title(watershed)
    plt.savefig(ext+watershed+'_discharges_2008.png')
    plt.clf()

# C2 watershed
create_topoflow_input_flow_files(flow_data,ext)
plot_flow_data(flow_data,ext)

# C3 watershed
#create_topoflow_input_flow_files(flow_data,ext,'C3')
#plot_flow_data(flow_data,ext,'C3')

# C4 watershed
#create_topoflow_input_flow_files(flow_data,ext,'C4')
#plot_flow_data(flow_data,ext,'C4')
