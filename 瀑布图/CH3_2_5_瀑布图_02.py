import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

# 示例数据
df = pd.DataFrame({
    'category': ['初始值', '增加1', '减少1', '增加2', '减少2', '最终值'],
    'value': [100, 20, -10, 30, -25, 115]
})

# 计算累积值
df['cumulative'] = df['value'].cumsum()  # .cumsum()方法计算累积值

# 绘制瀑布图
fig, ax = plt.subplots()

# 绘制正值条形图
ax.bar(df[df['value'] >= 0].index, df[df['value'] >= 0]['value'], color='green', label='增加')  # ax.bar()参数：x轴坐标，y轴坐标，颜色，标签，底部位置

# 绘制负值条形图
ax.bar(df[df['value'] < 0].index, df[df['value'] < 0]['value'], color='red', label='减少', bottom=df[df['value'] < 0]['cumulative'].shift(1).fillna(0))

# 添加标题和标签
ax.set_title('瀑布图示例')
ax.set_xlabel('类别')
ax.set_ylabel('值')
ax.legend()

# 显示图表
plt.show()
idebug = 1
