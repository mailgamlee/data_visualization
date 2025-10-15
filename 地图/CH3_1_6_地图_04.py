from geopandas import GeoDataFrame
import geoplot
import pandas as pd
from plotnine import *

# 1) 读取矢量地图数据（shapefile）
df_map = GeoDataFrame.from_file('Virtual_Map1.shp')
print("Virtual_Map1.shp:")
print(df_map)

# 2) 读取城市（或点）数据的 CSV 文件
df_city = pd.read_csv("Virtual_City.csv")
print("Virtual_City.csv:")
print(df_city)

# 3) 合并表格数据和地图几何数据
df = pd.merge(right=df_map, left=df_city, how='right', on="country")
df = GeoDataFrame(df)  # 转换为地图数据格式
# print(df)

# ----------------------------- 使用 plotnine（类似 ggplot）绘制地图 -----------------------------
# 说明：plotnine 中的 geom_map 通常与 map 数据配合，下面的写法利用 df 中的几何数据和属性进行渲染。
base_plot = (
    ggplot(df) +
    # geom_map 用于填充地图区域；aes(fill='orange') 指定使用 df 的 'orange' 列作为填充色（注意：'orange' 应是 df 的列名）
    geom_map(aes(fill='orange')) +
    # geom_text 在地图上添加文本标签；通过 aes 映射经度（long）、纬度（lat）与标签（country）
    geom_text(aes(x='long', y='lat', label='country'), colour="black", size=10) +
    # scale_fill_gradient2 用于设置填充色的三色渐变（低、中、高），并以 midpoint 指定中间值
    scale_fill_gradient2(low="#00A08A", mid="white", high="#FF0000", midpoint=df.orange.mean())
)

# 打印/渲染 plotnine 对象（在交互式环境中会显示图像；在某些 IDE/脚本环境中需保存为文件或显示窗口）
# print(base_plot)
base_plot.show()

# 辅助变量：用于在开发或调试时标记脚本末尾（无实际功能），可以安全删除或保留
test = 1
