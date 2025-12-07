# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 12:07:15 2019

@author: Jie Zhang，微信公众号【EasyShu】，本代码源自《Python数据可视化之美》
"""


import pandas as pd
import numpy as np
from plotnine import *
from pylab import mpl


import matplotlib.pyplot as plt
import matplotlib.patches as mpathes
from matplotlib.collections import PatchCollection

from matplotlib import cm,colors

mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

#-------------------------------(c)六角形.----------------------------------------------
#file = open('China_HexMap.csv',  errors='ignore') #encoding='utf-8', 
df=pd.read_csv('China_HexMap.csv',encoding='gb2312')
#file.close()  # 关闭文件


base_plot=(ggplot()+
geom_polygon(df,aes(x='x',y='y',group='Province'),colour="black",size=0.25,fill='w')+ #中国地图
geom_text(df.drop_duplicates('Province'),aes(x='Centerx', y='Centery-0.01',label='Province'),size=14,family='SimHei')+
#+scale_fill_cmap( name="Spectral_r")
#+theme_matplotlib()
theme(
    axis_title=element_text(size=18,face="plain",color="black"),
    axis_text = element_text(size=15,face="plain",color="black"),
    figure_size = (10, 10),
    dpi = 50))
print(base_plot)
i_stop = 1
