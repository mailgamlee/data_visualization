# import seaborn as sns

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

df = pd.read_csv('Line_Data.csv', index_col=0)

df.index = [datetime.strptime(d, '%Y/%m/%d').date() for d in df.index]

# ---------------------------------------------图6-1-1 多数据系列图. (a)折线图--------------------
fig = plt.figure(figsize=(5, 4), dpi=100)
plt.plot(df.index, df.AMZN, color='#F94306', label='AMZN')  # 程序原理、函数功能、重要参数
plt.plot(df.index, df.AAPL, color='#06BCF9', label='AAPL')
plt.xlabel("Year")  # 标签
plt.ylabel("Value")
plt.legend(loc='upper left', edgecolor='none', facecolor='none')  # 图例
plt.show()

# 格式要求：第一步、第二步、...

# 第一步：导入所需的库：pandas库用于数据处理、matplotlib库用于绘图、datetime库用于日期处理。
# 第二步：读取数据：pd.read_csv()函数，读取Line_Data.csv文件，index_col参数设置索引列为日期。
# 第三步：设置日期格式：datatime.strptime()函数，将日期字符串转换为日期格式。
# 第四步：设置图形大小、分辨率：plt.figure()函数，figsize参数设置图形大小，dpi参数设置分辨率。
# 第五步：绘制折线图：plt.plot()函数，x轴数据为df.index，y轴数据为df.AMZN、df.AAPL，color参数设置线条颜色，label参数设置线条标签。
# 第六步：设置坐标轴标签：plt.xlabel()函数、plt.ylabel()函数。
# 第七步：设置图例：plt.legend()函数，loc参数设置图例位置，edgecolor参数设置图例边框颜色，facecolor参数设置图例背景颜色。
# 第八步：显示图形：plt.show()函数。

# ----------------------------------------图6-1-1 多数据系列图.(b)面积图.-------------------------
columns = df.columns
colors = ["#F94306", "#06BCF9"]
fig = plt.figure(figsize=(5, 4), dpi=100)
plt.fill_between(df.index.values, y1=df.AMZN.values, y2=0, label=columns[1], alpha=0.75, facecolor=colors[0],
                 linewidth=1, edgecolor='k')
plt.fill_between(df.index.values, y1=df.AAPL.values, y2=0, label=columns[0], alpha=0.75, facecolor=colors[1],
                 linewidth=1, edgecolor='k')
plt.xlabel("Year")
plt.ylabel("Value")
plt.legend(loc='upper left', edgecolor='none', facecolor='none')
plt.show()

# 第一步：导入所需的库

# -------------------------------------图6-1-3 夹层填充面积图. (a)单色-----------------------------------------------------
df = pd.read_csv('Line_Data.csv')

df['date'] = [datetime.strptime(d, '%Y/%m/%d').date() for d in df['date']]
# df['date'].map(lambda x:datetime.datetime.strptime(x, '%Y/%m/%d').date())

df['ymin'] = df[['AMZN', 'AAPL']].apply(lambda x: x.min(), axis=1)
df['ymax'] = df[['AMZN', 'AAPL']].apply(lambda x: x.max(), axis=1)

fig = plt.figure(figsize=(5, 4), dpi=100)
plt.fill_between(df.date.values, y1=df.ymax.values, y2=df.ymin.values, alpha=0.15, facecolor='black', linewidth=1,
                 edgecolor='k')
plt.plot(df.date, df.AMZN, color='#F94306', label='AMZN')
plt.plot(df.date, df.AAPL, color='#06BCF9', label='AAPL')
plt.xlabel("Year")
plt.ylabel("Value")
plt.legend(loc='upper left', edgecolor='none', facecolor='none')
plt.show()

test = 1
