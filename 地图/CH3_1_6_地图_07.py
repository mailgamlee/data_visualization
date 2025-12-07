# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 11:04:56 2019

@author: Jie Zhang，微信公众号【EasyShu】，本代码源自《Python数据可视化之美》
"""
import geopandas as gpd

import geoplot.crs as gcrs
import numpy as np
import pandas as pd
from plotnine import *

df_map = gpd.GeoDataFrame.from_file('Virtual_Map1.shp')
df_city=pd.read_csv("Virtual_City.csv") 
 
df=pd.merge(right=df_map, left=df_city,how='right',on="country")
df=gpd.GeoDataFrame(df)

#------------------------------Method:plotnine --------------------------------------------------------
'''
base_plot=(ggplot(df)+
           geom_map(fill='white',color='gray')+
           geom_point(aes(x='long', y='lat',size='orange'),shape='o',colour="black",fill='#EF5439')+
           geom_text(aes(x='long', y='lat', label='city'),colour="black",size=10,nudge_y=-1.5)+
          scale_size(range=(2,9),name='price')
)
print(base_plot)
test = 1
'''
base_plot=(ggplot(df)+
           geom_map(fill='white',color='gray')+
           geom_point(aes(x='long', y='lat',size='orange',fill='orange'),shape='o',colour="black")+
           geom_text(aes(x='long', y='lat', label='city'),colour="black",size=10,nudge_y=-1.5)+
          #scale_fill_gradient2(low="#00A08A",mid="white",high="#FF0000",midpoint = df.orange.mean())
          scale_fill_cmap(name="YlOrRd")+
          scale_size(range=(2,9),name='price')
)
print(base_plot)
test = 1
