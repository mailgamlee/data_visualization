import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib import colors

# 1. 准备数据
df = pd.DataFrame(dict(labels=['LVS', 'SJM', 'MCE', 'Galaxy', 'MGM', 'Wynn'],
                       sizes=[24.20, 75.90, 12.50, 12.30, 8.10, 12.10],
                       inner_sizes=[15.10, 30.50, 5.00, 16.50, 4.00, 7.00]))

# 2. 数据处理
df = df.sort_values(by='sizes', ascending=False)
df = df.reset_index()

# 3. 颜色映射
cmap = plt.get_cmap('Reds_r', len(df))  # 获取一套颜色映射 Reds/Reds_r
color = [colors.rgb2hex(cmap(i)[:3]) for i in range(cmap.N)]  # 将颜色映射转换为十六进制颜色列表

# 4. 创建画布fig和子图ax
fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))   # 尺寸为6x3英寸，子图纵横比为1

# 5. 绘制环形图
'''
    ax.pie(x)函数 
    返回元组 (wedges, texts, autotexts)，分别对应饼图的三个核心组件：
    1. wedges： 代表饼图中的扇区;
    2. texts：对应饼图的类别标签;
    3. autotexts：对应饼图的数值标注
'''
# 绘制外环图
wedges_outer, texts = ax.pie(df['sizes'].values,  # pie饼图
                             radius=1,  # 半径
                             wedgeprops=dict(width=0.3, linewidth=0.5, edgecolor='k'),  # 边框属性
                             startangle=90,  # 开始角度
                             shadow=False,  # 阴影
                             counterclock=False,  # 中心对称
                             colors=color  # 颜色
                             )
# 绘制内环图
wedges_inner, texts = ax.pie(df['inner_sizes'].values,
                             radius=0.6,
                             wedgeprops=dict(width=0.3, linewidth=0.5, edgecolor='k'),
                             startangle=90,
                             shadow=False,
                             counterclock=False,
                             colors=color)

# 6. 标注外环图
bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)  # 边框类型
kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges_outer):
    ang = (p.theta2 - p.theta1) / 2 + p.theta1  # 计算扇区中心角度
    y = np.sin(np.deg2rad(ang))  # 角度转弧度后计算y坐标
    x = np.cos(np.deg2rad(ang))  # 角度转弧度后计算x坐标
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]  # 根据x正负确定文本对齐方式
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)  # 箭头连接样式
    kw["arrowprops"].update({"connectionstyle": connectionstyle})  # 更新箭头样式
    ax.annotate(df['labels'][i], xy=(x, y), xytext=(1.2 * x, 1.2 * y),
                horizontalalignment=horizontalalignment,
                arrowprops=dict(arrowstyle='-'))

# 7. 显示图表
plt.show()
