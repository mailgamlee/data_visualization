"""
Q-Q是一种散点图，横坐标为某一样本的分位数，纵坐标为另一样本的分位数，
横坐标与纵坐标组成的散点图代表同一个累计概率所对应的分位数。
若散点图在直线y=x附近分布，则这两个样本是同等分布；
若横坐标样本为标准正态分布且散点图是在直线y=x附近分布，
则纵坐标样本符合正态分布，且直线斜率代表样本标准差，截距代表样本均值
"""


import numpy as np
import pandas as pd
from plotnine import *

df = pd.DataFrame(dict(x=np.random.normal(loc=10,scale=1,size=250)))  # 随机生成正态分布数据

base_plot = (ggplot(df, aes(sample='x')) +         # plotnine自带的QQ图函数geom_qq()
    geom_qq(shape='o', fill="none") +
    geom_qq_line() +
    theme(
           # text=element_text(size=15,face="plain",color="black"),
           axis_title = element_text(size=18,face="plain",color="black"),
           axis_text = element_text(size=16,face="plain",color="black"),
           aspect_ratio =1.05,
           figure_size = (5,5),
           dpi = 100
          )
    )

# print(base_plot)
base_plot.show()
test = 1


