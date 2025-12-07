import plotly.express as px

data = dict(
    character=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
    value=[10, 14, 12, 10, 2, 6, 6, 4, 4],
    parent = ["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve"])

# .sunburst()函数用于绘制旭日图
fig = px.sunburst(
    data,
    names='character',
    parents='parent',
    values='value',
    # 数值，告诉 Plotly 使用 'value' 键来计算每个扇区（及其祖先）的大小。Plotly 旭日图的默认逻辑：每个父扇区的大小（角度宽度）是它自己的 value 加上所有后代（子节点、孙节点等）的 value 之和。
    title="旭日图 - 家族关系示例"
)
fig.show()
idebug = 1
