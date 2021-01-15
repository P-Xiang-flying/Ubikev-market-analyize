import pandas as pd
import os,sys
import csv
from multiprocessing import Process, Pool
def DTW_pool(eachColums,eachIndex):
    file = 'eachstation'
    dir = os.listdir(file)
    var ='lend'
    dataA = pd.read_csv(file+'/' + dir[eachColums])
    dataB = pd.read_csv(file + '/' + dir[eachIndex])
    timediff=DTW(dataA,dataB,var)
    print(str(eachColums)+'....'+str(eachIndex))
    return  [dir[eachColums],dir[eachIndex],timediff]
def DTW(dataA,dataB,var):
    timeMatrix =pd.DataFrame(columns = dataA.index,index= dataB.index)
    amountA = len(dataA)
    amountB =len(dataB)
    for eachA in range(0,amountA):
        for eachB in range(0,amountB):
            dynamicMax = 0
            if eachA>0:
                dynamicMax = timeMatrix.loc[eachA-1,eachB]
            if eachB>0:
                if dynamicMax < timeMatrix.loc[eachA,eachB-1]:
                    dynamicMax= timeMatrix.loc[eachA,eachB-1]
            if eachB > 0 and eachA>0:
                if dynamicMax < timeMatrix.loc[eachA-1,eachB-1]:
                    dynamicMax= timeMatrix.loc[eachA-1,eachB-1]
            timeMatrix.loc[eachA,eachB] =abs(dataA.loc[eachA,var]-dataB.loc[eachA,var])+dynamicMax
    return timeMatrix.loc[amountA-1,amountB-1]
def main():
    file = 'eachstation'
    dir = os.listdir(file)
    csvfile=open('diffmatrix_lend.csv', 'w', newline='',encoding='utf-8')
    writer = csv.writer(csvfile)
    pool = Pool(8)
    amount=(len(dir))
    list = []
    writer.writerow([
        'columns',
        'row',
        'value'
    ])
    for eachColums in range(0,amount):
    # for eachColums in range(0,10):
        for eachIndex in range(eachColums+1,amount):
        # for eachIndex in range(eachColums+1,10):
            list+=[(eachColums,eachIndex)]
    matrix =pool.starmap(DTW_pool,list)
    for eachdiff in matrix:
        writer.writerow(eachdiff)
    csvfile.close()
if __name__ == "__main__":
    main()