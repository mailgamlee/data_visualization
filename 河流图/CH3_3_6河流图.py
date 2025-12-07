import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm,colors
from matplotlib.pyplot import figure, show, rc

# ------------------------------------------(a)排序前----------------------------------------
df=pd.read_csv('StreamGraph_Data.csv',index_col =0)

labels=df.columns  # 取出列名作为标签
cmap=cm.get_cmap('Paired',11)  # get_cmap()函数用于从颜色映射表中获取颜色，参数为颜色名称、颜色数量
color=[colors.rgb2hex(cmap(i)[:3]) for i in range(cmap.N) ]
# 对于Paired颜色映射，取前3个元素作为颜色值
# colors.rgb2hex()函数用于将RGB颜色值转换为十六进制字符串

    
fig = figure(figsize=(5,4.5),dpi =90)     
plt.stackplot(df.index.values, df.values.T, labels=labels,baseline ='sym',colors=color,edgecolor='k',linewidth=0.25)
# plt.stackplot()函数用于绘制堆积图，参数为x轴数据、y轴数据、标签、颜色、边框颜色、边框宽度
plt.legend(loc="center right",
          bbox_to_anchor=(1.2, 0, 0, 1),title='Group',edgecolor='none',facecolor='none')
# plt.legend()函数用于设置图例，参数为位置(中心右)、边框(距离右边框1.2，距离底部0，宽度0，高度1)、标题、边框颜色、背景颜色

plt.show()
# fig.savefig('量化波形图1.pdf')

# --------------------------------------(b)排序后.-------------------------------------------
df=pd.read_csv('StreamGraph_Data.csv',index_col =0)
df_colmax= (df.apply(lambda x: x.max(), axis=0)).sort_values(ascending=True)  # 对于axis=0的x，求每列的最大值，并排序
N=len(df_colmax)
index=np.append(np.arange(0,N,2),np.arange(1,N,2)[::-1])  # 取奇数列和偶数列的索引
labels=df_colmax.index[index]

df=df[labels]

cmap=cm.get_cmap('Paired',11)
color=[colors.rgb2hex(cmap(i)[:3]) for i in range(cmap.N) ] 
    
fig = figure(figsize=(5,4.5),dpi =90)   
plt.stackplot(df.index.values, df.values.T, labels=labels,baseline ='wiggle',colors=color,edgecolor='k',linewidth=0.25)
plt.legend(loc="center right",
          bbox_to_anchor=(1.2, 0, 0, 1),title='Group',edgecolor='none',facecolor='none')
plt.show()
# fig.savefig('量化波形图2.pdf')
idebug = 1