import pandas as pd
import numpy as np
import csv
lendmatrix = pd.read_csv('diffmatrix_lend.csv')
rentmatrix =pd.read_csv('diffmatrix_rent.csv')
sortList = []
pointList=[]
pointPostion =[]
matrix = []
temp=[]
csvfile=open('diffmatrix.csv', 'w', newline='',encoding='utf-8')
writer = csv.writer(csvfile)
writer.writerow([
'columns','row','value'
])
for i in lendmatrix.index:
    pointList.append(lendmatrix['columns'][i])
    pointList.append(lendmatrix['row'][i])
pointList=list(set(pointList))
pointList.sort()
matrix =pd.DataFrame(columns=pointList,index=pointList)
matrix2 = pd.DataFrame(columns=pointList,index=pointList)
for i in lendmatrix.index:
    matrix.loc[lendmatrix['columns'][i],lendmatrix['row'][i]]=lendmatrix['value'][i]
    matrix.loc[lendmatrix['row'][i],lendmatrix['columns'][i]]=lendmatrix['value'][i]
for i in rentmatrix.index:
    matrix2.loc[rentmatrix['columns'][i],rentmatrix['row'][i]]=rentmatrix['value'][i]
    matrix2.loc[rentmatrix['row'][i],rentmatrix['columns'][i]]=rentmatrix['value'][i]
newdiff=matrix+matrix2
newdiff.to_csv('diffmatrix.csv')
x=newdiff.index
for i in range(0,len(newdiff)-1):
    for j in range(i+1,len(newdiff)):
        writer.writerow(
            [x[i],x[j],newdiff.loc[x[i]][x[j]]]
        )