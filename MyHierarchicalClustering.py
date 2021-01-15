import csv
import time
from os import write

import numpy as np
import pandas as pd
from numpy.lib.function_base import average
from numpy.ma.extras import average
from pandas.core.frame import DataFrame


class point:
    def __init__(self,name,pointList = []):
        self.name =name
        self.right=None
        self.left=None
        self.pointSet = pointList
        self.diff =0
    def merge(self,pointA,pointB,diff):
        self.left = pointA
        self.right = pointB
        self.pointSet = pointA.pointSet + pointB.pointSet
        self.diff =diff
def Clustering():
    diffList = pd.read_csv('diffmatrix.csv')
    sortList = []
    pointList=[]
    pointPostion =[]
    matrix = []
    temp=[]
    for i in diffList.index:
        pointList.append(diffList['columns'][i])
        pointList.append(diffList['row'][i])
    pointList=list(set(pointList))
    pointList.sort()
    for i in pointList:
        pointPostion.append(point(i,[i]))
    matrix =DataFrame(columns=pointList,index=pointList)
    for i in diffList.index:
        matrix.loc[diffList['columns'][i],diffList['row'][i]]=diffList['value'][i]
        matrix.loc[diffList['row'][i],diffList['columns'][i]]=diffList['value'][i]
    originalMatrix = matrix.copy()
    matrixLen=len(matrix.index)
    while matrixLen>1 :
        min=[99999,0,0]
        for rows in range(0,matrixLen):
            for columns in range(rows+1,matrixLen):
                if min[0] > matrix.iloc[rows,columns]:
                    min=[matrix.iloc[rows,columns],rows,columns]
        mergeA = pointList[min[1]]
        numA =str(mergeA).count('-')+1
        mergeB = pointList[min[2]]
        numB =str(mergeB).count('-')+1
        newNode = '('+str(mergeA)+'-'+str(mergeB)+')'
        tempPoint=point(newNode)
        tempPoint.merge(pointPostion[min[1]],pointPostion[min[2]],min[0])
        pointPostion[min[1]]=tempPoint
        del pointPostion[min[2]]
        for i in range(0,matrixLen):
            newDiff = (matrix.iloc[i,min[1]]*numA+matrix.iloc[i,min[2]]*numB)/(numA+numB)
            matrix.iloc[i,min[1]] = newDiff
            matrix.iloc[min[1],i] = newDiff
        matrix.rename(columns={mergeA:newNode},inplace=True)
        matrix.rename(index={mergeA:newNode},inplace=True)
        matrix = matrix.drop(columns=mergeB)
        matrix = matrix.drop(index=mergeB)
        pointList=matrix.index
        matrixLen-=1
    sortTree(pointPostion[0],originalMatrix)
    saveSort(pointPostion[0],sortList)
    saveTree(pointPostion,originalMatrix)
def saveTree(pointPostion,originalMatrix):
    max =[pointPostion[0],-100]
    pointNum = len(pointPostion)
    fileTree =open('HierarchicalClustering\\'+str(pointNum)+'.csv','w+', newline='')
    writer=csv.writer(fileTree)
    writer.writerow([
        'station_no',
        'class',
        'Diff'
        'normalized'
        ])
    nextDiff = 0
    for i in range(0,pointNum):
        if pointPostion[i].diff>max[1]:
            max=[i,pointPostion[i].diff]
        if i!=0:
            nextDiff += averageDiff(pointPostion[i].pointSet,pointPostion[i-1].pointSet,originalMatrix)
        for j in pointPostion[i].pointSet:
            writer.writerow([j,i,nextDiff])
    fileTree.close()
    if pointPostion[max[0]].left!= None:
        pointPostion.insert(max[0]+1,pointPostion[max[0]].right)
        pointPostion[max[0]]=pointPostion[max[0]].left
        saveTree(pointPostion,originalMatrix)
def saveSort(root,sortList):
    if root.left!=None:
        saveSort(root.left,sortList)
    else:
        sortList.append(root.name)
    if root.right !=None:
        saveSort(root.right,sortList)
def sortTree(root,originalmatrix):
    if root.left.left != None and root.left.right != None :
        leftLeftSet = root.left.left.pointSet
        leftRightSet = root.left.right.pointSet
        rightSet=root.right.pointSet
        if averageDiff(leftLeftSet,rightSet,originalmatrix)< averageDiff(leftRightSet,rightSet,originalmatrix):
            root.left.left,root.left.right = root.left.right,root.left.left
        sortTree(root.left,originalmatrix)
    if root.right.right != None and root.right.left != None :
        leftSet = root.left.pointSet
        rightLeftSet=root.right.left.pointSet
        rightRightSet=root.right.right.pointSet
        if averageDiff(rightRightSet,leftSet,originalmatrix)< averageDiff(rightLeftSet,leftSet,originalmatrix):
            root.right.right,root.right.left = root.right.left,root.right.right
        sortTree(root.right,originalmatrix)
def averageDiff(SetA,SetB,originalMatrix):
    count= 0
    sum=0
    for i in SetA:
        for j in SetB:
            count+=1
            sum += originalMatrix.loc[i,j]
    return sum/count
def main():
    Clustering()
if __name__ == "__main__":
    main()
