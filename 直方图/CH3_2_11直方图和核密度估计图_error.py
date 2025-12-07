import pandas as pd
#import numpy as np
#import seaborn as sns
from plotnine import *

file = open('Hist_Density_Data.csv') #encoding='utf-8',
df=pd.read_csv('Hist_Density_Data.csv')
file.close()  # 关闭文件

# --------------------------------------------(a2) 多数据系列直方图-----------------------------------

base_hist=(ggplot(df, aes(x='MXSPD', fill='Location'))+  
   geom_histogram(binwidth = 1,alpha=0.55,colour="black",size=0.25)+
   theme(
     text=element_text(size=13,color="black"),
     plot_title=element_text(size=15,family="myfont",face="bold.italic",hjust=.5,color="black"),#,
     legend_position=(0.7,0.8),
     legend_background = element_blank(),
     aspect_ratio =1.15,
     figure_size=(5,5)
   ))

base_hist.show()
test = 1

# ----------------------------------------(b2)多数据系列核密度估计图----------------------------------
base_density=(ggplot(df, aes(x='MXSPD',  fill='Location'))+
              geom_density(
                  bw=1,  # 带宽 - 控制平滑程度
                  alpha=0.55,  # 透明度 - 便于看到重叠
                  colour="black",  # 曲线边框颜色
                  size=0.25,  # 曲线边框粗细
                  kernel="gaussian"  # 使用高斯核函数
              )+
   theme(
     text=element_text(size=13,color="black"),
     plot_title=element_text(size=15,family="myfont",face="bold.italic",hjust=.5,color="black"),
     legend_position=(0.7,0.75),
     legend_background = element_blank(),
     aspect_ratio =1.15,
     figure_size=(5,5)
   ))
# print(base_density)
base_density.show()
test = 1
