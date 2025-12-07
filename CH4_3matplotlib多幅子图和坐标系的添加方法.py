from matplotlib import pyplot as plt  # 过程式接口or面向对象接口
import numpy as np

"""
maltplotlib多幅子图和坐标系的添加方法:
1. plt.subplot(子图编号, facecolor=颜色)
2. fig.add_subplot(子图编号, facecolor=颜色)
3. fig, ax = plt.subplots(ncols=列数, nrows=行数, figsize=(宽, 高))  # 返回figure对象和坐标轴
4. plt.subplot2grid((行数, 列数), (行, 列), colspan=跨列数, rowspan=跨行数, facecolor=颜色)

"""

# ----------------------------Method 1------------------------------------------------------------
# pyplot方式
plt.figure()  # 创建一个figure
# X = np.arange(0.01, 10, 0.01)  # .arange()函数用于生成一系列数字，在这里用于生成0.01-10之间，步长为0.01
# 分成2*2，占用第1个子图
plt.subplot(221, facecolor='#2B9ACE')  # plt.subplot()函数的第一个参数是子图编号，221表示2行2列的第1个子图；第二个参数为facecolor，设置子图背景颜色
# plt.plot(X, np.sin(X), 'r-')  # .plot()函数用于绘制曲线，第一个参数为x轴数据，第二个参数为y轴数据，第三个参数为线条颜色和线型

# 分成2*2，占用第2个子图
plt.subplot(222, facecolor='#89BD54')
# plt.plot(X, np.cos(X), 'g-')

# 分成2*1，占用第2个子图(即占用2*2第3、4子图)
plt.subplot(212, facecolor='#E6E243')
plt.bar(np.arange(6), np.array([2, 4, 1, 6, 3, 8]))  # .bar()函数用于绘制条形图，第一个参数为x轴数据，第二个参数为y轴数据
# plt.savefig('add_subplot1.pdf',format='pdf')
plt.suptitle('pyplot')  # 设置figure的标题
plt.show()


# -----------------------------Method 2-----------------------------------------------------------
# axes方式一：add_subplot
# 参数同plt.subplot一致
fig = plt.figure()
ax1 = fig.add_subplot(221,facecolor='#2B9ACE')  # fig.add_subplot()函数的第一个参数是子图编号，221表示2行2列的第1个子图；第二个参数为facecolor，设置子图背景颜色
# ax1.plot(X, np.sin(X), 'r-')

ax2 = fig.add_subplot(222,facecolor='#89BD54')
# ax2.plot(X, np.cos(X), 'g-')

ax3 = fig.add_subplot(212,facecolor='#E6E243')
# ax3.bar(np.arange(6), np.array([2, 4, 1, 6, 3, 8]))

fig.suptitle('add_subplot')
# plt.savefig('add_subplot2.pdf',format='pdf')
plt.show()

# -------------------------------Method 3---------------------------------------------------------
# axes方式二：subplots
# 相比add_subplot，函数调用比较简洁，但是不能自定义子图布局
fig = plt.figure()
fig, ax = plt.subplots(ncols=2, nrows=2, figsize=(8, 6))  # 创建一个figure，并创建2x2的子图，figsize设置子图大小
# X = np.arange(0.01, 10, 0.01)
# ax[0, 0].plot(X, 2 * X - 1)
ax[0, 0].set_facecolor("#8F4B99")

# ax[0, 1].plot(X, np.log(X))
ax[0, 1].set_facecolor("#89BD54")

# ax[1, 0].plot(X, np.exp(X))
ax[1, 0].set_facecolor("#E6E243")

# ax[1, 1].plot(X, np.sin(X))
ax[1, 1].set_facecolor("#2B9ACE")
  
# plt.savefig('add_subplot3.pdf',format='pdf')
fig.suptitle('subplots')
plt.show()

# ---------------------------Method 4-----------------------------------------------------------------
fig = plt.figure()
plt.subplot2grid((2,3),(0,0),colspan=2,facecolor='#2B9ACE')  # shape表示形状，loc表示位置，colspan表示跨列数，facecolor设置子图背景颜色
plt.subplot2grid((2,3),(0,2),facecolor='#E6E243')
plt.subplot2grid((2,3),(1,0),colspan=3,facecolor='#89BD54')
# plt.savefig('add_subplot4.pdf',format='pdf')
fig.suptitle('subplot2grid')
plt.show()

# 子图编号：
# (0,0) (0,1) (0,2)
# (1,0) (1,1) (1,2)
# ---------------------------Method 5-------------------------------------------------

# from pylab import *
import matplotlib.gridspec as gridspec  # gridspec模块用于创建复杂的子图布局
fig = plt.figure()
G = gridspec.GridSpec(2, 3)  # 创建一个2x3的网格布局

axes_1 = plt.subplot(G[0, 0:2],facecolor='#2B9ACE')  # G[0,0:2]表示第1行 第1列到第2列的子图；第二个参数为facecolor，设置子图背景颜色
# xticks([]), yticks([])
# text(0.5,0.5, 'Axes 1',ha='center',va='center',size=24,alpha=.5)

axes_2 = plt.subplot(G[0,2],facecolor='#E6E243')
# xticks([]), yticks([])
# text(0.5,0.5, 'Axes 2',ha='center',va='center',size=24,alpha=.5)

axes_3 = plt.subplot(G[1, :],facecolor='#89BD54')  # G[1,:]表示第2行 所有列的子图
# xticks([]), yticks([])
# text(0.5,0.5, 'Axes 3',ha='center',va='center',size=24,alpha=.5)

# plt.savefig("add_subplot5.pdf")
# plt.savefig('../figures/gridspec.png', dpi=64)
fig.suptitle('gridspec')
plt.show()


# -----------------------------Method 6-------------------------------------------------
fig = plt.figure()  # 创建一个全新空白图表对象，后续所有的 plt.xxx 函数调用都会作用于这个 fig 对象，因为它是当前的 figure
plt.axes([0.1,0.1,.8,.8],facecolor='#E6E243')
# plt.axes()函数用于设置坐标轴范围和背景颜色,参数为[左,下,宽,高],facecolor设置子图背景颜色
# 参数 [left, bottom, width, height]用来手动指定新创建的 Axes 在 Figure 中的位置和大小：从 Figure 左边 10%，下边 10% 的位置开始，宽度和高度都为 Figure 的 80%。
# plt.xticks([]), plt.yticks([])
# plt.text(0.6,0.6, 'axes([0.1,0.1,.8,.8])',ha='center',va='center',size=20,alpha=.5)

plt.axes([0.2,0.2,.3,.3],facecolor='#2B9ACE')
# plt.xticks([]), plt.yticks([])
# plt.text(0.5,0.5, 'axes([0.2,0.2,.3,.3])',ha='center',va='center',size=16,alpha=.5)
# plt.savefig("add_subplot6.pdf")
# plt.plt.savefig("../figures/axes.png",dpi=64)
plt.show()

# ------------------------------Method 7-----------------------------------------
fig = plt.figure()
plt.axes([0.1,0.1,.5,.5],facecolor='#8F4B99')
# plt.xticks([]), plt.yticks([])
# plt.text(0.1,0.1, 'axes([0.1,0.1,.8,.8])',ha='left',va='center',size=16,alpha=.5)

plt.axes([0.2,0.2,.5,.5],facecolor='#89BD54')
# plt.xticks([]), plt.yticks([])
# plt.text(0.1,0.1, 'axes([0.2,0.2,.5,.5])',ha='left',va='center',size=16,alpha=.5)

plt.axes([0.3,0.3,.5,.5],facecolor='#E6E243')
# plt.xticks([]), plt.yticks([])
# plt.text(0.1,0.1, 'axes([0.3,0.3,.5,.5])',ha='left',va='center',size=16,alpha=.5)

plt.axes([0.4,0.4,.5,.5],facecolor='#2B9ACE')
# plt.xticks([]), plt.yticks([])
# plt.text(0.1,0.1, 'axes([0.4,0.4,.5,.5])',ha='left',va='center',size=16,alpha=.5)

# plt.savefig("add_subplot7.pdf")
plt.show()

test = 1
