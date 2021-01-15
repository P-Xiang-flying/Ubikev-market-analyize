import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd
import matplotlib as mpl
import os
def Linebystation():
    file ='HierarchicalClustering'
    DataNum=pd.read_csv('weekdata.csv',encoding='utf-8')
    DataNum['timeNum']=DataNum['week']*24+DataNum['hour']
    for i in range(1,369):
        cmap = cm.rainbow
        locationData=pd.read_csv(file+'\\'+str(i)+'.csv',encoding='utf-8')
        locationData.reindex(index=locationData.index[::-1])
        max = locationData['Diff'].max()
        locationData['normalized']= (locationData['Diff']/max)
        locationData['R']=0
        locationData['G']=0
        locationData['B']=0
        # norm = mpl.colors.Normalize(vmin=min_val, vmax=max_val)
        color_list = cmap(locationData['normalized'])
        count=0
        for j in locationData.index:
            temp=color_list[count]
            locationData.loc[j,'R']=temp[0]
            locationData.loc[j,'G']=temp[1]
            locationData.loc[j,'B']=temp[2]
            count+=1
        for j in locationData.index:
            station =locationData.loc[j,'station_no']
            mask = DataNum['station_no']==station
            temp=DataNum[mask]
            RGB = (locationData.loc[j,'R'],locationData.loc[j,'G'],locationData.loc[j,'B'],1)
            plt.plot(temp['timeNum'],temp['rent'],color=RGB,ls='-', lw=1)
            plt.plot(temp['timeNum'],-temp['lend'],color=RGB,ls='-', lw=1)
        plt.title('class:'+str(i))
        plt.savefig('eachline\\'+str(i)+'.png')
        plt.close()
        # for i in stationlist:
        #     print(i[1])
        #     temp = i[1]
            
        #     plt.plot(temp['timeNum'],-temp['lend'],color='black',ls='--', lw=1,zorder=1)
        # plt.show()
    # for i in dir:
    #     Data=pd.read_csv(file+'\\'+i,encoding='utf-8')
    #     Data['week']=0
    #     Data['hour']=0
    #     for j in Data.index:
    #         temp = Data['station_no'][j].split('-')
    #         Data['week'][j]=temp[0]
    #         Data['hour'][j]=temp[1]
    #     temp = pd.merge(DataNum, Data, on=["week", "hour"]).reset_index()
        
    #     plt.scatter(temp['timeNum'],temp['rent'] ,c=temp['Diff'],cmap='rainbow',zorder=2,s=15)
    #     plt.scatter(temp['timeNum'],-temp['lend'] ,c=temp['Diff'],cmap='rainbow',zorder=2,s=15)
    #     plt.title(str(i).replace('.csv',''))
    #     plt.savefig('plt_line\\'+str(i).replace('.csv','')+'.png')
    #     plt.close()
def Calendar():
    file ='HierarchicalClustering'
    dir = os.listdir(file)
    for i in dir:
        Data=pd.read_csv(file+'\\'+i,encoding='utf-8')
        Data['week']=0
        Data['hour']=0
        for j in Data.index:
            temp = Data['station_no'][j].split('-')
            Data['week'][j]=temp[0]
            Data['hour'][j]=temp[1]
        p1=plt.scatter(Data['week'], Data['hour'],c=Data['Diff'],cmap='rainbow')
        plt.title(str(i).replace('.csv',''))
        plt.savefig('plt\\'+str(i).replace('.csv','')+'.png')
        p1.remove()
def Linechart():
    file ='HierarchicalClustering'
    dir = os.listdir(file)
    DataNum=pd.read_csv('weekGroup.csv',encoding='utf-8')
    DataNum['timeNum']=DataNum['week']*24+DataNum['hour']
    plt.plot(DataNum['timeNum'],DataNum['rent'],color='black',ls='--', lw=1,zorder=1)
    plt.plot(DataNum['timeNum'],-DataNum['lend'],color='black',ls='--', lw=1,zorder=1)
    for i in dir:
        Data=pd.read_csv(file+'\\'+i,encoding='utf-8')
        Data['week']=0
        Data['hour']=0
        for j in Data.index:
            temp = Data['station_no'][j].split('-')
            Data['week'][j]=temp[0]
            Data['hour'][j]=temp[1]
        temp = pd.merge(DataNum, Data, on=["week", "hour"]).reset_index()
        p1=plt.scatter(temp['timeNum'],temp['rent'] ,c=temp['Diff'],cmap='rainbow',zorder=2,s=15)
        p2=plt.scatter(temp['timeNum'],-temp['lend'] ,c=temp['Diff'],cmap='rainbow',zorder=2,s=15)
        plt.title(str(i).replace('.csv',''))
        plt.savefig('plt_line\\'+str(i).replace('.csv','')+'.png')
        p1.remove()
        p2.remove()
# Linechart()
# Calendar()
Linebystation()