import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib_venn import venn3, venn3_circles

plt.rcParams['font.sans-serif'] = ['SimHei'] # 用来正常显示中文标签

# 初始化布局
fig = plt.figure(figsize=(8,8))

# 自定义标签
plt.subplot(2, 2, 1) 
v=venn3(subsets = (10, 8, 22, 6,9,4,2), set_labels = ('Group A', 'Group B', 'Group C'))
v.get_label_by_id('A').set_text('My Favourite group!')
plt.title('自定义标签')


# 自定义圆圈
plt.subplot(2, 2, 2) 
v=venn3(subsets = (10, 8, 22, 6,9,4,2), set_labels = ('Group A', 'Group B', 'Group C'))
c=venn3_circles(subsets = (10, 8, 22, 6,9,4,2), linestyle='dashed', linewidth=1, color="grey")
plt.title('自定义圆圈')


# 自定义单组
plt.subplot(2, 2, 3) 
v=venn3(subsets = (10, 8, 22, 6,9,4,2), set_labels = ('Group A', 'Group B', 'Group C'))
c=venn3_circles(subsets = (10, 8, 22, 6,9,4,2), linestyle='dashed', linewidth=1, color="grey")
c[0].set_lw(8.0)
c[0].set_ls('dotted')
c[0].set_color('skyblue')
plt.title('自定义单组')

# 自定义背景色
plt.subplot(2, 2, 4) 
v=venn3(subsets = (10, 8, 22, 6,9,4,2), set_labels = ('Group A', 'Group B', 'Group C'))
plt.gca().set_facecolor('skyblue')
plt.gca().set_axis_on()
plt.title('自定义背景色')

plt.show()
idebug = 1