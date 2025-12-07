# eve 代表根节点，在最中间位置作饼图，颜色为白色
# parent 代表父节点，在中间层（senth蓝色、cain橙色、awan绿色、abel紫色、azura黄色【低饱和颜色更美观】）
# character 代表子节点，在最外层，以父节点的色系的不同透明度填充

# 从数据中可以看出父子对应关系：
# eve(根节点) -> senth(父节点) -> enos(叶子节点)
# eve(根节点) ->  senth(parent) -> noam(character)
# eve(根节点) -> cain(叶子节点)
# eve(根节点) -> awan(parent) -> enoch(character)
# eve(根节点) -> abel(parent)
# eve(根节点) -> azura(parent)
# eve(根节点) -> ""(空白叶子节点)

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import colors
import numpy as np

# --- 1. 常量与配置 ---
LINEWIDTH = 2.0
EDGECOLOR = 'w'
FONTSIZE = 10
FONTWEIGHT = 'bold'
TOTAL_VALUE = 68

PARENT_COLORS = {
    "Seth": "#4A8BB8",  # 更深的蓝色
    "Cain": "#E99742",  # 更深的橙色
    "Awan": "#5CA85C",  # 更深的绿色
    "Abel": "#9B78B4",  # 更深的紫色
    "Azura": "#FDD36A",  # 更深的黄色
    "": "#FFFFFF"
}


# --- 2. 数据准备与计算函数 ---
def prepare_data(df, total_value, parent_colors):
    """准备和计算 Level 1, Level 2, Level 3 的值、标签和颜色。"""

    # Level 1 数据
    root_label = ["Eve"]
    root_values = [total_value]

    # Level 2 数据计算 (值 = 自身 + 子节点总和)
    level2_data_map = {}
    parent_order = ['Seth', 'Cain', 'Abel', 'Awan', 'Azura']

    for char in parent_order:
        own_value = df[df['character'] == char]['value'].iloc[0]
        children_sum = df[df['parent'] == char]['value'].sum()
        level2_data_map[char] = own_value + children_sum

    level2_values = [level2_data_map[char] for char in parent_order]
    level2_labels = parent_order.copy()

    # 添加空白占位符
    blank_value = total_value - sum(level2_values)
    level2_values.append(blank_value)
    level2_labels.append("")
    level2_colors = [parent_colors.get(c, '#E0E0E0') for c in level2_labels]

    # Level 3 数据生成配置 (子节点名称, 值, 父节点, 透明度)
    level3_children_config = [
        ('Enos', 10, 'Seth', 0.6),  # 透明度 0.6
        ('Noam', 2, 'Seth', 0.3),  # 透明度 0.3
        ('Enoch', 4, 'Awan', 0.6)  # 透明度 0.6
    ]

    level3_values = []
    level3_display_labels = []
    level3_colors = []
    transparent_indices = set()
    current_index = 0

    # 遍历 Level 2 顺序，生成 Level 3 扇区
    for i, parent in enumerate(level2_labels):
        parent_value = level2_values[i]
        children = [c for c in level3_children_config if c[2] == parent]
        filled_value = 0

        if children:
            # 1. 填充真实子节点
            for label, val, _, alpha in children:
                level3_values.append(val)
                level3_display_labels.append(label)
                level3_colors.append(colors.to_rgba(parent_colors[parent], alpha=alpha))
                filled_value += val
                current_index += 1

            # 2. 添加剩余部分的透明占位符
            remainder = parent_value - filled_value
            if remainder > 0:
                level3_values.append(remainder)
                level3_display_labels.append('')
                if parent == "":
                    level3_colors.append(parent_colors[""])
                else:
                    level3_colors.append(colors.to_rgba(parent_colors[parent], alpha=0))
                    transparent_indices.add(current_index)
                current_index += 1
        else:
            # 3. 父节点自身充当占位符 (Cain, Abel, Azura, Blank)
            level3_values.append(parent_value)
            level3_display_labels.append('')
            if parent == "":
                level3_colors.append(parent_colors[""])
            else:
                level3_colors.append(colors.to_rgba(parent_colors[parent], alpha=0))
                transparent_indices.add(current_index)
            current_index += 1

    return (root_label, root_values, level2_labels, level2_values, level2_colors,
            level3_display_labels, level3_values, level3_colors, transparent_indices)


# 自定义函数：计算扇区中心位置 (弧度)
def get_label_coordinates(wedge, radius):
    """根据楔形对象计算标签的中心 (x, y) 坐标"""
    angle_center = (wedge.theta2 + wedge.theta1) / 2
    angle_rad = np.deg2rad(angle_center)
    x = radius * np.cos(angle_rad)
    y = radius * np.sin(angle_rad)
    return x, y


# --- 3. 绘图函数 ---

def draw_sunburst_chart(data_pack):
    """绘制旭日图并进行标签后处理。"""

    (root_label, root_values, level2_labels, level2_values, level2_colors,
     level3_display_labels, level3_values, level3_colors, transparent_indices) = data_pack

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(aspect="equal"))
    ax.set_title("Family Tree Sunburst Chart", fontsize=16, pad=20)

    wedge_props = {"width": 0.4, "edgecolor": EDGECOLOR, "linewidth": LINEWIDTH}
    transparent_wedge_props = {"width": 0.4, "edgecolor": 'none', "linewidth": 0}

    # === Level 1: 根节点 ===
    wedges_root, texts_root = ax.pie(
        root_values,
        labels=root_label,
        radius=0.4,
        colors=["#FFFFFF"],
        wedgeprops=wedge_props,
        startangle=90,
        labeldistance=0
    )
    if texts_root:
        eve_text_object = texts_root[0]
        eve_text_object.set_position((0, 0))
        eve_text_object.set_ha('center')
        eve_text_object.set_va('center')
        eve_text_object.set_fontsize(FONTSIZE)
        eve_text_object.set_fontweight(FONTWEIGHT)

    # === Level 2: 父节点 ===
    wedges_level2, _ = ax.pie(
        level2_values,
        labels=[''] * len(level2_values),
        radius=0.8,
        colors=level2_colors,
        wedgeprops=wedge_props,
        startangle=90
    )

    # Level 2 标签后处理：精确居中
    for i, wedge in enumerate(wedges_level2):
        label = level2_labels[i]
        if label != "":
            # 标签中心半径为 0.6
            x, y = get_label_coordinates(wedge, radius=0.6)
            ax.text(x, y, label,
                    ha='center', va='center',
                    fontsize=FONTSIZE, fontweight=FONTWEIGHT)
        else:
            # 移除空白扇区边框
            wedge.set(**transparent_wedge_props)

    # === Level 3: 子节点 ===
    wedges_level3, _ = ax.pie(
        level3_values,
        labels=[''] * len(level3_values),
        radius=1.2,
        colors=level3_colors,
        wedgeprops=wedge_props,
        startangle=90
    )

    # Level 3 标签和边框后处理
    for i, wedge in enumerate(wedges_level3):
        label = level3_display_labels[i]

        if label != "":
            # 标签中心半径为 1.0
            x, y = get_label_coordinates(wedge, radius=1.0)
            ax.text(x, y, label,
                    ha='center', va='center',
                    fontsize=FONTSIZE, fontweight=FONTWEIGHT)

        # 移除透明/空白扇区的边框
        if i in transparent_indices or level3_colors[i] == PARENT_COLORS[""]:
            wedge.set(**transparent_wedge_props)

    ax.axis('equal')
    plt.show()


# --- 4. 主执行流程 ---
if __name__ == '__main__':
    # 原始数据
    raw_data = dict(
        character=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
        parent=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve"],
        value=[10, 14, 12, 10, 2, 6, 6, 4, 4])

    df = pd.DataFrame(raw_data)

    # 1. 准备和计算数据
    sunburst_data = prepare_data(df, TOTAL_VALUE, PARENT_COLORS)

    # 2. 绘制图表
    draw_sunburst_chart(sunburst_data)