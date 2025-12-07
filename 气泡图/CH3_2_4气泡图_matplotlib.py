from plotnine.data import mtcars  # 自带数据
import matplotlib.pyplot as plt

x=mtcars['wt']
y=mtcars['mpg']
size=mtcars['disp']
fill=mtcars['disp']

fig, ax = plt.subplots(figsize=(5,4))
scatter = ax.scatter(x, y, c=fill, s=size, linewidths=0.5, edgecolors="k",cmap='RdYlBu_r')  # ax.scatter()函数用于绘制散点图

cbar = plt.colorbar(scatter)  # plt.colorbar()函数用于生成颜色条
cbar.set_label('disp')

handles, labels = scatter.legend_elements(prop="sizes", alpha=0.6,num=5 )
# scatter.legend_elements()函数用于生成不同大小的点的颜色和大小,参数prop="sizes"表示根据size值来设置颜色和大小,num=5表示生成5个不同大小的点
ax.legend(handles, labels, loc="upper right", title="Sizes")

plt.show()
idebug = 1