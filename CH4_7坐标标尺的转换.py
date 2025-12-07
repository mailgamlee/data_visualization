import pandas as pd
import numpy as np
from plotnine import *
# from plotnine.data import *
import matplotlib.pyplot as plt
import matplotlib


# plt.rc('font',family='Times New Roman')  # 这是另一种设置matplotlib字体的方式
matplotlib.rcParams['font.family'] = 'Times New Roman'  # 设置matplotlib的全局字体为Times New Roman，这会影响到plotnine的输出

# 读取数据
df = pd.read_csv("logarithmic_scale.csv")  # 使用pandas的read_csv函数从CSV文件中读取数据，并存储在名为df的DataFrame中

# 数据重塑（宽格式 -> 长格式）
# pd.melt(数据集, id_vars=ID变量列表, value_vars=数值变量列表, var_name=新变量名, value_name=新值名)
# 指定id_vars参数将它们保留为列，并将其他变量展开为新的行（通过定义var_name和value_name参数来指定新列名）
df_melt = pd.melt(df, id_vars='VIN(V)', var_name='Class', value_name='value')

# 创建第一个图表（线性Y轴）
p1 = (ggplot(df_melt, aes(x='VIN(V)', y='value', color='Class')) +  # ggplot(数据集, aes(x=X轴变量, y=Y轴变量, color=颜色变量))

      geom_line(size=1) +  # geom_line(线型，大小)绘制折线图
      scale_x_continuous(breaks=np.arange(-20, 21, 5), limits=(-20, 20)) +  # scale_x_continuous(breaks=刻度值列表, limits=X轴范围)
      scale_y_continuous(breaks=np.arange(0, 2.1, 0.5), limits=(0, 2)) +  # scale_y_continuous(breaks=刻度值列表, limits=Y轴范围)
      scale_color_manual(values=("#36BED9", "#FF0000")) +  # scale_color_manual(values=颜色值列表)设置颜色值
      theme_classic() +  # 设置主题为经典主题

      theme(
          text=element_text(size=12, colour="black"),  # 设置图表中所有文本（如轴标签、刻度标签、图例）的大小为12，颜色为黑色。
          panel_grid_major=element_line(color="#C7C7C7", linetype='--'),  # 添加主要网格线。颜色是浅灰色(#C7C7C7)，线型是虚线(--)。
          aspect_ratio=0.8,  # 设置图表的宽高比为0.8（高度/宽度）。
          dpi=100,  # 设置图表的分辨率为100 DPI。
          figure_size=(5, 5),  # 设置图表的尺寸为5x5英寸。
          legend_position=(0.8, 0.8),  # 设置图例的位置。(0.8, 0.8)是一个相对坐标，分别对应图表宽度和高度的80%处，即右上角。
          legend_background=element_rect(fill="none")  # 设置图例的背景为透明（fill="none"）。
      )
      )

p1.show()  # 显示第一个图表。
# p1.save("logarithmic_scale1.pdf")

# 创建第二个图表（对数Y轴）
p2 = (ggplot(df_melt, aes(x='VIN(V)', y='value', color='Class')) +
      geom_line(size=1) +
      scale_x_continuous(breaks=np.arange(-20, 21, 5), limits=(-20, 20)) +
      scale_y_log10(name='log(value)', limits=(0.00001, 10)) +
      scale_color_manual(values=("#36BED9", "#FF0000")) +
      theme_classic() +
      theme(
          text=element_text(size=12, colour="black"),
          panel_grid_major=element_line(color="#C7C7C7", linetype='--'),
          aspect_ratio=0.8,
          dpi=100,
          figure_size=(5, 5),
          legend_position=(0.8, 0.8),
          legend_background=element_rect(fill="none")
      )
      )
p2.show()  # 显示第二个图表。
# p1.save("logarithmic_scale2.pdf")

test = 1
