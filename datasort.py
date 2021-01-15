import csv
import os
import time
# dataSort().TimeData()
# dataSort().diifData()
from operator import index
from optparse import Values
import pandas as pd
from numpy.lib.function_base import append
from numpy.lib.index_tricks import diag_indices_from
from pandas.core.indexes.datetimes import date_range


class DataSort(object):
    timeList =''
    stationdata = ''
    stationList=''
    def __init__(self,timefile='time_list.csv',datafile='station_data.csv',locationfile='location.csv'):
        self.timeList = pd.read_csv(timefile)
        self.stationdata = pd.read_csv(datafile)
        self.stationList = pd.read_csv(locationfile,encoding = "utf-8")

    def StationData(self,goal = 'eachstation') :
        diffData=pd.DataFrame()
        for eachStation in self.stationList['station_no']:
            mask = self.stationdata['station_no']==eachStation
            eachStationData = self.stationdata[mask]
            eachStationData.to_csv(goal+'\\'+str(eachStation)+'.csv',index =False)
            print(str(eachStation)+'done')
    def diffData(self):
        diffData=pd.DataFrame()
        for eachStation in self.stationList['station_no']:
            mask = self.stationdata['station_no']==eachStation
            eachStationData = self.stationdata[mask]
            eachStationData['diff']=eachStationData['avalible_spaces'].diff()
            eachStationData['rent'] = eachStationData['diff']
            eachStationData['lend'] = -eachStationData['diff']
            eachStationData.rent[eachStationData['rent']<=0]=0
            eachStationData.lend[eachStationData['lend']<=0]=0
            diffData=diffData.append(eachStationData,ignore_index =True)
            print(str(eachStation)+'done')
        diffData.to_csv('diffdata.csv',index = False)
    def TimeData(self):
        for eachTime in self.timeList['time_id']:
            mask = self.stationdata['time_id']==eachTime
            eachTimeData = self.stationdata[mask]
            eachTimeData.to_csv('eachtime\\'+str(eachTime)+'.csv',index =False)
            print(str(eachTime)+'done')
    def timeStruct(self):
        self.timeList['week']=0
        self.timeList['hour']=0
        self.timeList['weekDays']=0
        for eachTime in self.timeList.index:
            structtime = time.strptime(self.timeList['time'][eachTime],'%Y/%m/%d %H:%M')
            self.timeList['week'][eachTime] = structtime.tm_wday
            self.timeList['weekDays'][eachTime] =0 if structtime.tm_wday>4 else 1
            self.timeList['hour'][eachTime] = structtime.tm_hour
            self.timeList['number']=0
        f = open('weekList.csv','w',newline='',encoding='utf-8')
        writer=csv.writer(f)
        weekList = self.timeList.groupby(by=['week','hour'])
        writer.writerow([
            'time_id',
            'week',
            'hour',
        ])
        for i in weekList:
            writer.writerow([
                str(i[0][0])+'-'+str(i[0][1]),
                i[0][0],
                i[0][1]
            ])
        self.timeList.to_csv('time_list.csv',index = False)
    def addtimeID(self,goal='weekData.csv'):
        temp = pd.read_csv(goal)
        temp['time_id']=0
        for i in temp.index:
            temp.loc[i,'time_id'] = str(temp.loc[i,'week'])+'-'+str(temp.loc[i,'hour'])
        temp.to_csv(goal,index=False)
    def sumByWeek(self):
        weekData=self.stationdata.merge(self.timeList, left_on='time_id', right_on='time_id')
        weekRent = weekData.groupby(by=['week','hour','station_no'])['rent'].sum()
        weekLend = weekData.groupby(by=['week','hour','station_no'])['lend'].sum()
        weekData=pd.merge(weekRent, weekLend, on=["week", "hour",'station_no']).reset_index()
        weekData.to_csv('weekData.csv',index=False)
    def weekDataWithLocation(self):
        weekData=pd.merge(self.stationdata,self.stationList , on=['station_no']).reset_index()
        weekData=weekData.drop(['status', 'name','district','address','parking_spaces'], axis=1)
        weekData.to_csv('weekData.csv',index=False)
    def weekDatabyGroup(self):
        weekRent = self.stationdata.groupby(by=['week','hour'])['rent'].sum()
        weekLend = self.stationdata.groupby(by=['week','hour'])['lend'].sum()
        weekData=pd.merge(weekRent, weekLend, on=["week", "hour"]).reset_index()
        weekData.to_csv('weekGroup.csv',index=False)
# test = DataSort(locationfile='location_taipai.csv')
# test.diffData()
# test.timeStruct()
# test = DataSort(datafile='diffdata.csv',locationfile='location_taipai.csv')
# test.sumByWeek()
# test.addtimeID('weekData.csv')
test = DataSort(timefile='weekList.csv',datafile='weekData.csv',locationfile='location_taipai.csv')
# test.StationData(goal = 'eachstation')
# test.TimeData()
# test.weekDataWithLocation()
test.weekDatabyGroup()