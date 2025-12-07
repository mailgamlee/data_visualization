#coding=UTF-8
# 导入所需的库
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as image

# 正常显示中文标签
mpl.rcParams['font.sans-serif'] = ['SimHei']

# 自动适应布局
mpl.rcParams.update({'figure.autolayout': True})

# 正常显示负号
mpl.rcParams['axes.unicode_minus'] = False


# 使用「面向对象」的方法画图
fig, ax = plt.subplots(figsize=(8, 2.6))

# 设置标题和坐标轴标签
ax.set_title("2020年3月，销售收入超额完成目标\n", fontsize=26, verticalalignment='bottom')

# 定义指标名称
y = '销售收入'

# 背景放在最底层
ax.barh(y, 200, height=0.8, color='#00589F', alpha=0.40, label='差')
ax.barh(y, 50, height=0.8, left=200, color='#00589F', alpha=0.25, label='中')
ax.barh(y, 50, height=0.8, left=250, color='#00589F', alpha=0.1, label='好')

# 隐藏的占位元素，为了让图片留有更多的空白区域
ax.barh(y, 50, height=1, left=250, color='#00589F', alpha=0)

# 实际值
ax.barh(y, 280, height=0.3, color='#00589F', label='实际')

# 目标值
lc = ax.vlines(260, -0.3, 0.3, color='#CC5036', label='目标')
# 设置线条宽度
lc.set_linewidth(3)

# 隐藏边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

# X 轴的刻度线朝内，调整线条的长度，让其贴近条形图
mpl.rcParams['xtick.direction'] = 'in'
ax.tick_params(axis='x', which='major', length=8)

# 隐藏 Y 轴刻度
ax.set_yticks([])

# 设置 X 轴标签
ax.set_xlabel('\n（单位：万元）', fontsize=16)

# 设置坐标标签字体大小
ax.tick_params(labelsize=20)

# 设置图例显示的位置
ax.legend(bbox_to_anchor=(1.15, 1.15))

# 在另一个坐标轴中添加 LOGO 图片
#im = image.imread('./data/linji.jpg')
ax2 = fig.add_axes([0.75, -0.15, 0.08, 0.26])
#ax2.imshow(im, aspect='auto', extent=(0, 1, 0, 1), zorder=-1)
# 隐藏刻度线
ax2.set_xticks([])
ax2.set_yticks([])
# 隐藏边框
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax2.spines['left'].set_visible(False)

# 设置字体
font={'family':'SimHei', 'color':'#00589F', 'size':15}

# 标示制图的作者信息
ax2.text(1, 0.2, ' 制图：\n' + r'$@$' + '数据化分析', fontdict=font)

plt.show()
idebug = 1