import pandas as pd
import numpy as np
from plotnine import *
from plotnine.data import *
import matplotlib.pyplot as plt

df = pd.DataFrame(dict(segment=["A", "B", "C", "D"],
                       Alpha=[2400, 1200, 600, 250],
                       Beta=[1000, 900, 600, 250],
                       Gamma=[400, 600, 400, 250],
                       Delta=[200, 300, 400, 250]))
df = df.set_index('segment')
melt_df = pd.melt(df.reset_index(), id_vars=["segment"], var_name='variable', value_name='value')

df_rowsum = df.apply(lambda x: x.sum(), axis=1)  # df.apply()函数沿着 DataFrame 的某个轴应用一个函数，参数包括 axis 和 func。

for i in df_rowsum.index:
    for j in df.columns:
        df.loc[i, j] = df.loc[i, j] / df_rowsum[i] * 100

df_rowsum = df_rowsum / np.sum(df_rowsum) * 100
df['xmax'] = np.cumsum(df_rowsum)  # 横坐标上限
df['xmin'] = df['xmax'] - df_rowsum  # 横坐标下限

dfm = pd.melt(df.reset_index(), id_vars=["segment", "xmin", "xmax"], value_name="percentage")
# pd.melt()函数，将数据框转换为长格式，参数有三个，第一个参数为数据框，第二个参数为id_vars，即id变量，第三个参数为value_name，即值变量。

dfm['ymax'] = dfm.groupby('segment')['percentage'].transform(lambda x: np.cumsum(x))
dfm['ymin'] = dfm.apply(lambda x: x['ymax'] - x['percentage'], axis=1)

dfm['xtext'] = dfm['xmin'] + (dfm['xmax'] - dfm['xmin']) / 2
dfm['ytext'] = dfm['ymin'] + (dfm['ymax'] - dfm['ymin']) / 2

# join()函数，连接两个表格data.frame
dfm = pd.merge(left=melt_df, right=dfm, how="left", on=["segment", "variable"])

df_label = pd.DataFrame(
    dict(x=np.repeat(102, 4), y=np.arange(12.5, 100, 25), label=["Alpha", "Beta", "Gamma", "Delta"]))

base_plot = (ggplot() +
             geom_rect(aes(ymin='ymin', ymax='ymax', xmin='xmin', xmax='xmax', fill='variable'),
                       # geom_rect(aes(ymin = 'ymin', ymax = 'ymax', xmin = 'xmin', xmax = 'xmax'),
                       dfm, colour="black") +
             geom_text(aes(x='xtext', y='ytext', label='value'), dfm, size=10) +
             geom_text(aes(x='xtext', y=103, label='segment'), dfm, size=13) +
             geom_text(aes(x='x', y='y', label='label'), df_label, size=10, ha='left') +
             scale_x_continuous(breaks=np.arange(0, 101, 25), limits=(0, 110)) +
             # scale_fill_hue(s = 0.90, l = 0.65, h=0.0417,color_space='husl')+
             theme(  # panel_background=element_blank(),
                 panel_grid_major=element_line(colour="grey", size=.25, linetype="dotted"),
                 panel_grid_minor=element_line(colour="grey", size=.25, linetype="dotted"),
                 # panel_grid_major = element_line(colour = "white",size=.25,linetype ="dotted" ),
                 # panel_grid_minor = element_line(colour = "white",size=.25,linetype ="dotted" ),
                 text=element_text(size=10),
                 legend_position="none",
                 aspect_ratio=1.,
                 figure_size=(5, 5),
                 dpi=100
             ))

print(base_plot)
# 将plotnine图形转换图形
base_plot.show()
test = 1
