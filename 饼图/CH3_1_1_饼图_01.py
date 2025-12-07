import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors

# -------------------------------------图(d)-----------------------------------------------
df = pd.DataFrame(dict(labels=['LVS', 'SJM', 'MCE', 'Galaxy', 'MGM', 'Wynn'],
                       sizes=[24.20, 75.90, 12.50, 12.30, 8.10, 12.10]))
df = df.sort_values(by='sizes', ascending=False)  # 按sizes列降序排列
df = df.reset_index()  # 重置索引

cmap = plt.get_cmap('Reds_r', 6)  # 获取颜色映射
color = [colors.rgb2hex(cmap(i)[:3]) for i in range(cmap.N)]
# color=["#ffffff", "#ffffff","#ffffff","#ffffff","#ffffff","#ffffff" ]  # 自定义颜色

fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

wedges, texts = ax.pie(df['sizes'].values,
                       startangle=90, shadow=False, counterclock=False, colors=color,
                       wedgeprops={'width': 0.3, 'linewidth': 0.3, 'edgecolor': 'k'})  # 圆环图
# wedgeprops=dict(linewidth=0.5, edgecolor='k'))  # 扇形图
# 说明返回参数的作用：
# wedges：扇形的列表，包含每个扇形的相关信息
# texts：文本标签的列表，包含每个文本标签的相关信息

bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1) / 2. + p.theta1  # 计算扇区中心角度
    y = np.sin(np.deg2rad(ang))  # 角度转弧度后计算y坐标
    x = np.cos(np.deg2rad(ang))  # 角度转弧度后计算x坐标
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]  # 根据x正负确定文本对齐方式
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)  # 箭头连接样式
    kw["arrowprops"].update({"connectionstyle": connectionstyle})  # 更新箭头样式
    ax.annotate(df['labels'][i], xy=(x, y), xytext=(1.2 * x, 1.2 * y),
                horizontalalignment=horizontalalignment,
                arrowprops=dict(arrowstyle='-'))

plt.show()

# 第一步：导入必要的库：pandas用于数据处理，简写为pd；numpy用于数学计算，简写为np；matplotlib用于绘图，简写为plt。
# 第二步：准备数据：使用pd.DataFrame()函数创建数据框，包含labels和sizes两列，将两列用字典形式传入。
# 第三步：数据处理：使用pd.sort_values()函数对数据框按sizes列降序排列，函数包括by和ascending两个参数，使用pd.reset_index()函数重置索引。
# 第四步：设置颜色：使用plt.get_cmap()函数获取颜色映射，参数包括颜色映射名称和数量。对于每个颜色映射，使用colors.rgb2hex()函数将RGB颜色转换为HEX颜色。


# ---------------------------------------图(a)指定顺序------------------------------------------------

df = pd.DataFrame(dict(labels=['LVS', 'SJM', 'MCE', 'Galaxy', 'MGM', 'Wynn'],
                       sizes=[24.20, 75.90, 12.50, 12.30, 8.10, 12.10]))
df = df.sort_values(by='sizes', ascending=False)
df = df.reset_index()

index = np.append(0, np.arange(df.shape[0] - 1, 0, -1))
df = df.iloc[index, :]
df = df.reset_index()

cmap = plt.get_cmap('Reds_r', 6)
color = [colors.rgb2hex(cmap(i)[:3]) for i in index]
# color=["#ffffff", "#ffffff","#ffffff","#ffffff","#ffffff","#ffffff" ]

fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

# fig1, ax1 = plt.subplots()
wedges, texts = ax.pie(df['sizes'].values,  # labels=df['labels'],
                       startangle=90, shadow=True, counterclock=False, colors=color,
                       wedgeprops=dict(linewidth=0.5, edgecolor='k'))  # , labels=labels, autopct='%1.1f%%',
# shadow=False, startangle=0,wedgeprops =dict(linewidth=0.5, edgecolor='k'))
# plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    print(i)
    ang = (p.theta2 - p.theta1) / 2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax.annotate(df['labels'][i], xy=(x, y), xytext=(1.2 * x, 1.2 * y),  # xytext=(1.35*np.sign(x), 1.4*y),
                horizontalalignment=horizontalalignment,
                arrowprops=dict(arrowstyle='-'))

plt.show()
