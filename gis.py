import os
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
class gis(object):
    def imgForHierarchicalClustering(self):
        crs = {'init': 'epsg:4326'}
        gdf_Rail=gpd.read_file('TaiwanMap\\taipai.shp',encoding='utf-8')
        file = 'HierarchicalClustering'
        for i in range(0,369):
            locationData=pd.read_csv(file+'\\'+str(i)+'.csv',encoding='utf-8')
            geom = [Point(xy) for xy in zip(locationData.lng, locationData.lat)]
            gdf = gpd.GeoDataFrame(locationData, crs=crs, geometry=geom)
            base=gdf_Rail.boundary.plot(color='black',figsize=(30,30))
            gdf.plot(cmap='rainbow',ax=base,markersize=80, legend=True,column='Diff')
            plt.title('class:'+str(i),size=150)
            plt.savefig('map\\'+str(i)+'.png')
            plt.close()
    def imgForAllTime(self):
        Data=pd.read_csv('weekData.csv',encoding='utf-8')
        crs = {'init': 'epsg:4326'}
        for i in range(0,7):
            for j in range(0,24):
                if i !=1 and (j<11 or j>15):
                    gdf_Rail=gpd.read_file('TaiwanMap\\taipai.shp',encoding='utf-8')
                    maskA=Data['week']==i
                    temp =Data[maskA]
                    maskB=temp['hour']==j
                    temp=temp[maskB]
                    geom = [Point(xy) for xy in zip(temp.lng, temp.lat)]
                    gdf = gpd.GeoDataFrame(temp, crs=crs, geometry=geom)
                    base=gdf_Rail.plot()
                    gdf.plot(cmap='Greens',ax=base,markersize=0.5, legend=True,column='rent',vmax=40,vmin = 0)
                    plt.title('week:'+str(i)+',hour:'+str(j))
                    plt.savefig('map_rent\\'+str(i)+'-'+str(j)+'.png')
test =gis()
test.imgForHierarchicalClustering()