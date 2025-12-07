import scipy.cluster.hierarchy as shc
import numpy as np
from matplotlib import cm,colors
from matplotlib import pyplot as plt
import pandas as pd
from plotnine.data import mtcars
from sklearn.preprocessing import scale
plt.rcParams['axes.facecolor']='w'  # 设置背景色为白色
plt.rc('axes',axisbelow=True)    # 显示坐标轴


df=mtcars.set_index('name')  # 设置索引为车辆名称
df.loc[:,:] = scale(df.values )  # 标准化数据，存到df中。df.loc[:,:]表示对df的每行每列进行操作。
# df.iloc[]表示对df的每行进行操作
# df.loc[]表示对df的每列进行操作

# -------------------------------------------横向树形图-----------------------------------------------

fig=plt.figure(figsize=(10, 10), dpi= 80)
dend = shc.dendrogram(shc.linkage(df,method='ward'), orientation='left',
                      labels=df.index.values, color_threshold=5
                      )
# shc.dendrogram()函数来自scipy库，shc.dendrogram(metrix, method='ward', labels=labels, orientation='left', color_threshold=5)
# 第一个参数是距离矩阵，第二个参数是聚类方法，第三个参数是树的方向，第四个参数是标签，第五个参数是颜色阈值。
# 这里的距离矩阵是通过shc.linkage()函数计算的，这里使用的是Ward距离，聚类方法是ward，树的方向是左侧，标签是df.index.values，颜色阈值是5。
# 颜色阈值是指树的分支颜色变化的阈值，如果距离变化超过这个阈值，则分支颜色会变化。

# 绘制树形图
plt.xticks(fontsize=13,rotation=0)  # 设置横坐标标签的字体大小和旋转角度
plt.yticks(fontsize=14)  # 设置纵坐标标签的字体大小
# plt.grid(color='gray',which='major', axis='x',linestyle='--')  # 设置网格线

ax = plt.gca()  # plt.gca()作用是获取当前坐标轴，以便于设置坐标轴的属性。当前坐标轴用plt.xticks()和plt.yticks()设置。
ax.spines['left'].set_color('none')  # 去掉左边框
ax.spines['right'].set_color('none')  # 去掉右边框
ax.spines['top'].set_color('k')  # 上边框颜色设置为黑色
ax.spines['bottom'].set_color('k')  # 下边框颜色设置为黑色

#plt.savefig('树状图1.pdf')
plt.show()

# -------------------------------------------纵向树形图-----------------------------------------------
fig=plt.figure(figsize=(5, 5), dpi= 80)
# plt.title("USArrests Dendograms", fontsize=22)
dend = shc.dendrogram(shc.linkage(df.values.T,method='ward'), orientation='top',
                      labels=df.columns.values, color_threshold=5,
                      )
plt.xticks(fontsize=13,rotation=0)
plt.yticks(fontsize=14)
# plt.grid(color='gray',which='major', axis='y',linestyle='--')

ax = plt.gca()
ax.spines['left'].set_color('k')
ax.spines['right'].set_color('k')
ax.spines['top'].set_color('none')
ax.spines['bottom'].set_color('none')

# plt.savefig('树状图2.pdf')
plt.show()
idebug = 1