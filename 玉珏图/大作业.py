"""
热力图 + 气泡图 ：
可用于电商库存监控与销售分析场景，同时展示了两个关键业务维度：
背景颜色代表各商品类别在不同季度的库存周转率（红色越深表示销售越快），
而黄色气泡的大小则显示实际库存数量（气泡越大库存越多）。
可以快速识别哪些商品需要紧急补货，哪些存在积压风险，从而优化采购策略、预防缺货或过剩
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# 设置 matplotlib 字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 设置数据
np.random.seed(42)
rows = ['A', 'B', 'C', 'D', 'E']
cols = ['Q1', 'Q2', 'Q3', 'Q4']

"""
行（A, B, C, D, E）：不同商品类别
A：电子产品
B：服装服饰
C：家居用品
D：美妆护肤
E：食品饮料
列（Q1, Q2, Q3, Q4）：2024年的四个季度
Q1：第一季度（1-3月）
Q2：第二季度（4-6月）
Q3：第三季度（7-9月）
Q4：第四季度（10-12月）
"""

# 维度 1 (背景颜色): 周转率数据 (例如：库存周转率)
data_color = pd.DataFrame(
    np.random.randint(50, 100, size=(len(rows), len(cols))),
    index=rows,
    columns=cols
)

# 维度 2 (气泡大小): 实际库存数据 (例如：库存数量)
data_size = pd.DataFrame(
    np.random.randint(10, 50, size=(len(rows), len(cols))),
    index=rows,
    columns=cols
)

scale_factor = 35  # 缩放因子

# 创建图表
plt.figure(figsize=(10, 8))

# 绘制热力图 (表示 data_color 的数据)
ax = sns.heatmap(
    data_color,
    cmap='Reds',
    annot=False,
    linewidths=.15,
    linecolor='k',
    cbar_kws={
        'label': '库存周转率',
        'shrink': 0.7,  # 颜色条高度缩为原来的80%
        'aspect': 12,  # 颜色条宽高比（数值越大越细）
        'pad': 0.04,  # 颜色条与热力图的间距
        'anchor': (0.1, 0.0),  # 颜色条的锚点：(1,0) = 颜色条右下角对齐目标位置
    }
)

# 调整标签样式，在绘制后单独设置
if ax.collections[0].colorbar is not None:
    cbar = ax.collections[0].colorbar  # 获取颜色条对象
    # 设置标签及其样式
    cbar.set_label('库存周转率', labelpad=10, fontsize=12)  # 这里可以调整字体大小

# 获取热力图的索引和列名用于定位气泡
x_coords = np.arange(len(cols)) + 0.5  # 加0.5是为了居中显示
y_coords = np.arange(len(rows)) + 0.5

# 绘制气泡
for i, row_name in enumerate(rows):
    for j, col_name in enumerate(cols):
        # 气泡中心位置
        x_center = x_coords[j]
        y_center = y_coords[i]

        # 气泡大小
        size = data_size.loc[row_name, col_name]

        # 使用 scatter 绘制气泡
        plt.scatter(
            x_center,
            y_center,
            s=size * scale_factor,  # 面积=库存数量*缩放因子
            color='yellow',
            alpha=0.7,
            edgecolors='black',
            zorder=2
        )

        # 可选：在气泡中心显示数值
        plt.text(
            x_center,
            y_center,
            str(size),
            ha='center',
            va='center',
            fontsize=12,
            color='black',
            weight='bold',
            zorder=3
        )

# 设置图表标题和标签
plt.title('气泡热力图', loc='center', fontsize=14, pad=20)
ax.set_yticklabels(rows, rotation=0)

# 为气泡大小添加图例
for size_val in [10, 30, 50]:
    plt.scatter(
        [],
        [],
        s=size_val * scale_factor,
        color='yellow',
        alpha=0.8,
        edgecolors='black',
        label=f'{size_val}'
    )

plt.legend(
    scatterpoints=1,  # 每个图例项显示1个散点
    frameon=False,  # 去掉图例边框
    labelspacing=4,  # 图例项纵向间距
    title='库存数量',  # 图例标题
    handletextpad=1.8,  # 气泡与文字的间距
    loc='upper left',  # 图例基准位置
    bbox_to_anchor=(1.06, 1.1),  # 图例偏移（x=1.05右移，y=0.65下移）
    alignment='center',
    title_fontsize=12
)

plt.tight_layout()
plt.show()
