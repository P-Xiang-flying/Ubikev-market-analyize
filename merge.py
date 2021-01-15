import pandas as pd
import os

from pandas.core.reshape.merge import merge
def MergeByFile(file,right='location.csv'):
    dir = os.listdir(file)
    stationData = pd.read_csv(right,encoding='utf-8')
    for eachstep in dir:
        temp=pd.read_csv(file + '\\'+eachstep)
        Data=pd.merge(temp, stationData, on=['station_no']).reset_index()
        Data.to_csv(file+'\\'+eachstep,index=False)
def MergeAndAdd(right,left,by,newVar,rightVar,leftVar,saveName):
    rightData = pd.read_csv(right)
    leftData = pd.read_csv(left)
    Data = pd.merge(rightData, leftData, on=by).reset_index()
    Data[newVar]=Data[rightVar]+Data[leftVar]
    Data.to_csv(saveName,index=False)
# MergeAndAdd('diffmatrix_lend.csv','diffmatrix_rent.csv',['columns','row'],'value','value_x','value_y','diffmatrix.csv')
MergeByFile(file = 'HierarchicalClustering',right='location_taipai_justxy.csv')