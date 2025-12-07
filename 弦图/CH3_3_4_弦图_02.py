from pycirclize import Circos
import pandas as pd
import matplotlib.pyplot as plt

# 定义行名和列名
row_names = ["S1", "S2", "S3"]
col_names = ["E1", "E2", "E3", "E4", "E5", "E6"]

# 矩阵数据 - 表示S行和E列之间的关系强度
matrix_data = [
    [4, 14, 13, 17, 5, 2],   # S1与E1-E6的关系值
    [7, 1, 6, 8, 12, 15],    # S2与E1-E6的关系值
    [9, 10, 3, 16, 11, 18],  # S3与E1-E6的关系值
]

# 创建DataFrame，便于数据处理
matrix_df = pd.DataFrame(matrix_data, index=row_names, columns=col_names)

# 初始化Circos图
circos = Circos.initialize_from_matrix(
    matrix_df,        # 输入矩阵数据
    start=-265,       # 起始角度(-265度)
    end=95,           # 结束角度(95度)
    space=5,          # 扇区间隔5度
    r_lim=(93, 100),  # 半径范围(93-100)
    cmap="tab10",     # 颜色映射方案
    label_kws=dict(r=94, size=12, color="white"),  # 标签参数
    link_kws=dict(ec="black", lw=0.5),             # 连接线参数
)

print(matrix_df)
fig = circos.plotfig()
# fig.show()
# idebug = 1
plt.show(block=True)
