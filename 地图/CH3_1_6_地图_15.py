import geopandas as gpd
from shapely.geometry import Point
import numpy as np
import pandas as pd
from plotnine import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib as mpl

df_map = gpd.GeoDataFrame.from_file('Virtual_Map0.shp')

long_mar=np.arange(105,135, 0.6)  # 定义经度范围
lat_mar=np.arange(30,60, 0.8)  # 定义纬度范围
X,Y=np.meshgrid(long_mar,lat_mar)  # meshgrid()函数用于生成网格数据
df_grid =pd.DataFrame({'long':X.flatten(),'lat':Y.flatten()})  # 展平网格数据

geom = gpd.GeoSeries([Point(x, y) for x, y in zip(df_grid.long.values, df_grid.lat.values)])  # 创建点对象
df_grid=gpd.GeoDataFrame(df_grid,geometry=geom)  # geodataframe()是专门用于处理地理空间数据的数据结构

# ------------- GeoDataFrame 和 DataFrame 用法详解--------------
"""
# 创建一个普通的 DataFrame
data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
df = pd.DataFrame(data)

# 创建一个 GeoDataFrame
geometry = [Point(1, 1), Point(2, 2), Point(3, 3)]
gdf = gpd.GeoDataFrame(data, geometry=geometry)

输出结果：
   A  B
0  1  4
1  2  5
2  3  6
   A  B                 geometry
0  1  4   POINT (1.00000 1.00000)
1  2  5   POINT (2.00000 2.00000)
2  3  6   POINT (3.00000 3.00000)

"""

inter_point = df_map['geometry'].intersection(df_grid['geometry'].union_all()).tolist()
# intersection()求交集；tolist()转为列表

point_x=[]
point_y=[]
for i in range(len(inter_point)):
    if str(type(inter_point[i]))!= "<class 'shapely.geometry.point.Point'>":
        for j in range(len(inter_point[i].geoms)):
            point_x=point_x + [inter_point[i].geoms[j].x]
            point_y=point_y + [inter_point[i].geoms[j].y]
        # point_x=point_x+[item.x for item in inter_point[i]]
        # point_y=point_y+[item.y for item in inter_point[i]]
    else:
        point_x=point_x+[inter_point[i].x]
        point_y=point_y+[inter_point[i].y]

df_pointmap =pd.DataFrame({'long':point_x,'lat':point_y})

# ------------------------------------------------------------------------------------------

df_huouse=pd.read_csv("Virtual_huouse.csv")

long_mar = np.arange(105, 135 + 0.6, 0.6)  # 边界定义，生成经度边界数组，范围从105到135.6，步长为0.6
lat_mar = np.arange(30, 60 + 0.8, 0.8)  # 边界定义，生成纬度边界数组，范围从30到60.8，步长为0.8

# np.histogram2d()用于计算二维直方图
"""
# 参数1: df_huouse.long.values - 输入数据的经度值
# 参数2: df_huouse.lat.values - 输入数据的纬度值
# 参数3: (long_mar, lat_mar) - 二维直方图的边界，分别为经度边界和纬度边界
# 返回值: hist - 二维直方图数组，表示在每个经度-纬度区间内的数据点数量
#         xedges - 经度边界数组
#         yedges - 纬度边界数组
"""
hist, xedges, yedges = np.histogram2d(df_huouse.long.values, df_huouse.lat.values, (long_mar, lat_mar))

long_mar = np.arange(105, 135, 0.6)  # 重新定义经度边界数组，范围从105到135，步长为0.6
lat_mar = np.arange(30, 60, 0.8)  # 重新定义纬度边界数组，范围从30到60，步长为0.8

# np.meshgrid()用于生成网格数据
"""
参数1: lat_mar - 纬度边界数组
参数2: long_mar - 经度边界数组
返回值: Y - 维度为 (len(lat_mar), len(long_mar)) 的二维数组，表示纬度值
        X - 维度为 (len(lat_mar), len(long_mar)) 的二维数组，表示经度值
"""
Y, X = np.meshgrid(lat_mar, long_mar)

# 将网格数据转换为DataFrame格式
"""
np.ravel() 函数用于将多维数组转换为一维数组
参数: hist.ravel() - 将二维直方图数组转换为一维数组
参数: X.ravel() - 将经度网格数组转换为一维数组
参数: Y.ravel() - 将纬度网格数组转换为一维数组
"""
df_gridmap = pd.DataFrame({'long': X.ravel(), 'lat': Y.ravel(), 'count': hist.ravel()})

# plt.imshow(hist)  # 使用plt.imshow()显示二维直方图

# pd.merge()用于合并两个DataFrame，示例
"""
df_gridmap
long	lat	count
105	30	10
105	30.8	5
105.6	30	3

df_pointmap
long	lat	other_data
105	30	A
105	30.8	B
106	30	C

合并后的 df_gridmap
long	lat	count	other_data
105	30	10	A
105	30.8	5	B
105.6	30	3	NaN
"""
df_gridmap = pd.merge(df_gridmap, df_pointmap, how='left', on=['long', 'lat'])

# ------------------------------------------------------------------------------------------

fig = plt.figure(figsize=(7,8),dpi =150)  # 创建一个figure对象，设置大小为7x8，分辨率为150
ax = fig.add_subplot(111, projection='3d')  # 创建一个三维坐标轴，参数111表示1行1列的第一个子图，projection参数表示投影方式
ax.view_init(azim=50, elev=20)  # 改变绘制图像的视角,即相机的位置,azim沿着z轴旋转，elev沿着y轴
ax.grid(False)  # grid函数用于是否隐藏坐标轴的网格线(false表示不隐藏)

ax.xaxis._axinfo['tick']['outward_factor'] = 0  # 设置x轴刻度线向外延伸的长度为0
ax.xaxis._axinfo['tick']['inward_factor'] = 0.4  # 设置x轴刻度线向内延伸的长度为0.4
ax.yaxis._axinfo['tick']['outward_factor'] = 0  # 设置y轴刻度线向外延伸的长度为0
ax.yaxis._axinfo['tick']['inward_factor'] = 0.4  # 设置y轴刻度线向内延伸的长度为0.4
ax.zaxis._axinfo['tick']['outward_factor'] = 0  # 设置z轴刻度线向外延伸的长度为0
ax.zaxis._axinfo['tick']['inward_factor'] = 0.4  # 设置z轴刻度线向内延伸的长度为0.4
ax.xaxis.pane.fill = False  # 设置x轴坐标平面不填充颜色
ax.yaxis.pane.fill = False  # 设置y轴坐标平面不填充颜色
ax.zaxis.pane.fill = False  # 设置z轴坐标平面不填充颜色
ax.xaxis.pane.set_edgecolor('none')  # 设置x轴坐标平面的边框颜色为无（即不显示边框）
ax.yaxis.pane.set_edgecolor('none')  # 设置y轴坐标平面的边框颜色为无（即不显示边框）
ax.zaxis.pane.set_edgecolor('none')  # 设置z轴坐标平面的边框颜色为无（即不显示边框）

ax.zaxis.line.set_visible(False)  # 隐藏z轴的线
ax.set_zticklabels([])  # 设置z轴的刻度标签为空
ax.set_zticks([])  # 设置z轴的刻度为空

dx=df_gridmap.long.values  # 从df_gridmap数据框中提取经度(long)列的值
dy=df_gridmap.lat.values  # 从df_gridmap数据框中提取纬度(lat)列的值
dz=df_gridmap['count'].values  # 从df_gridmap数据框中提取计数(count)列的值

plt.xlim(min(dx),max(dx))  # 设置x轴的显示范围为经度的最小值到最大值
plt.ylim(min(dy),max(dy))  # 设置y轴的显示范围为纬度的最小值到最大值
plt.margins(0,0,0)  # 设置图形的边距，这里设置为无边距

ax.set_xlabel( "long")  # 设置x轴标签为"经度"
ax.set_ylabel("lat")  # 设置y轴标签为"纬度"
# ax.set_zlabel("count") # 注释掉的代码，原本用于设置z轴标签为"计数"

zpos = 0 # 设置z轴的位置为0

colors = cm.Reds(dz / float(max(dz)))  # 根据计数值dz的大小，使用Reds颜色映射生成对应的颜色数组，颜色强度从0到1

ax.bar3d(dx, dy, zpos, 0.5, 0.5, dz, color=colors,  # 使用bar3d函数绘制三维柱状图，参数分别为x位置、y位置、z位置、x宽度、y宽度、z高度和颜色
         alpha=1,edgecolor='k',linewidth=0.1,zsort='average')  # 设置透明度、边缘颜色、线条宽度和柱子排序方式

ax2 = fig.add_axes([0.85, 0.35, 0.025, 0.15])  # 在图形中添加一个新的坐标轴，用于绘制颜色条，参数为坐标轴的位置和大小
cmap = mpl.cm.Reds  # 设置颜色映射为Reds
norm = mpl.colors.Normalize(vmin=0, vmax=1)  # 设置颜色映射的归一化对象，将0到1的数值映射到颜色条上
bounds = np.arange(min(dz),max(dz),2)  # 设置颜色条的界限，从dz的最小值到最大值，步长为2
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)  # 根据设定的界限重新设置颜色映射的归一化对象，使颜色条与dz的值匹配
cb2 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap,norm=norm,boundaries=bounds,  # 创建颜色条对象，参数包括坐标轴、颜色映射、归一化对象和界限
ticks=np.arange(min(dz),max(dz),2),spacing='proportional',label='count')  # 设置颜色条的刻度值和标签
# fig.savefig('三维统计直方地图1.pdf')

plt.show()  # 显示图形
test = 1  # 测试变量，这里赋值为1
