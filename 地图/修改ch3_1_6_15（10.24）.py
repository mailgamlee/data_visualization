import geopandas as gpd
from shapely.geometry import Point
import numpy as np
import pandas as pd
from plotnine import *
from plotnine.coords import coord_fixed

# ----------------------------- 数据准备 ----------------------------

df_map = gpd.GeoDataFrame.from_file('Virtual_Map0.shp')

long_mar = np.arange(105, 135, 0.6)
lat_mar = np.arange(30, 60, 0.8)
X, Y = np.meshgrid(long_mar, lat_mar)
df_grid = pd.DataFrame({'long': X.flatten(), 'lat': Y.flatten()})

geom = gpd.GeoSeries([Point(x, y) for x, y in zip(df_grid.long.values, df_grid.lat.values)])
df_grid = gpd.GeoDataFrame(df_grid, geometry=geom)

# 计算地图区域和网格点的交集
inter_point = df_map['geometry'].intersection(df_grid['geometry'].union_all()).tolist()

point_x = []
point_y = []

for i in range(len(inter_point)):
    current_geom = inter_point[i]
    geom_type = current_geom.geom_type

    # 如果是单个 Point
    if geom_type == 'Point':
        point_x = point_x + [current_geom.x]
        point_y = point_y + [current_geom.y]

    # 如果是集合类型 (MultiPoint 或 GeometryCollection)
    elif geom_type in ('MultiPoint', 'GeometryCollection'):
        if hasattr(current_geom, 'geoms'):
            for sub_geom in current_geom.geoms:
                if sub_geom.geom_type == 'Point':
                    point_x = point_x + [sub_geom.x]
                    point_y = point_y + [sub_geom.y]
    # 忽略其他几何类型（如 LineString, Polygon, Empty 等）

df_pointmap = pd.DataFrame({'long': point_x, 'lat': point_y})

# ------------------------------------------------------------------------------------------

df_huouse = pd.read_csv("Virtual_huouse.csv")

long_mar = np.arange(105, 135 + 0.6, 0.6)
lat_mar = np.arange(30, 60 + 0.8, 0.8)

# 计算 2D 直方图（房屋数量）
hist, xedges, yedges = np.histogram2d(df_huouse.long.values, df_huouse.lat.values, (long_mar, lat_mar))

long_mar = np.arange(105, 135, 0.6)
lat_mar = np.arange(30, 60, 0.8)

Y, X = np.meshgrid(lat_mar, long_mar)

df_gridmap = pd.DataFrame({'long': X.ravel(), 'lat': Y.ravel(), 'count': hist.ravel()})

df_gridmap = pd.merge(df_gridmap, df_pointmap, how='left', on=['long', 'lat'])

# ------------------------ 标签数据和图例精细控制的准备 ---------------------------------
# 1. 准备国家/地区标签数据 (修复缺失的定义)
df_country_centers = df_huouse.groupby('country').agg(
    long_center=('long', 'mean'),
    lat_center=('lat', 'mean')
).reset_index()

# 2. 计算图例刻度
min_count = df_gridmap['count'].min()
max_count = df_gridmap['count'].max()

# 刻度步长为 2
custom_breaks = np.arange(0, max_count + 2, 2)
if max_count not in custom_breaks:
    custom_breaks = np.append(custom_breaks, max_count).astype(int)

custom_breaks = np.unique(custom_breaks)
custom_breaks = custom_breaks[custom_breaks <= max_count]

# ------------------------ 2D 平铺热力图 (使用 plotnine) ---------------------------------

base_plot = (
        ggplot()
        # 1. 绘制热力图 (geom_tile)
        + geom_tile(
            data=df_gridmap[df_gridmap['count'] > 0],
            mapping=aes(x='long', y='lat', fill='count'),
            inherit_aes=False,
            color=None  # 移除瓦片边界
)
        # 2. 绘制地图边界（覆盖在热力图上方）
        + geom_map(
            data=df_map,
            fill=None,
            color='black',
            size=0.5,
            inherit_aes=False
)
        # 3. 设置填充颜色渐变 (精细控制图例)
        + scale_fill_cmap(
            cmap_name='Blues',
            name='Count',
            breaks=custom_breaks.tolist(),
            labels=custom_breaks.astype(str).tolist()
)
        # 4. 添加国家/地区名称标签
        + geom_text(
            data=df_country_centers,
            mapping=aes(x='long_center', y='lat_center', label='country'),
            inherit_aes=False,
            color='purple',
            size=12,
            fontweight='bold'
)
        # 5. 修正地图的坐标比例
        + coord_fixed(ratio=1)
        # 6. 设置图表标题和坐标轴标签
        + labs(
            title="House Count Distribution Heatmap (2D)",
            x="Longitude",
            y="Latitude"
)
        # 7. 调整主题
        + theme_bw()
        # 移除图表背景网格线
        + theme(panel_grid_major=element_blank(),
                panel_grid_minor=element_blank())
)

# 显示图形
base_plot.show()