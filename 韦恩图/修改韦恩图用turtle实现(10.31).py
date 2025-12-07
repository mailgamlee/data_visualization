import turtle
import math

# --- 配置绘图窗口和画笔 ---
screen = turtle.Screen()
screen.setup(width=600, height=600)
screen.title("Turtle 绘制三圆韦恩图")
t = turtle.Turtle()
t.speed(0)  # 设置最快速度
t.hideturtle()  # 隐藏海龟图标

# --- 绘图参数 ---
RADIUS = 100  # 圆的半径
CENTER_X_OFFSET = 70
CENTER_Y_OFFSET = 50

# 三个圆的圆心坐标
center_a = (-CENTER_X_OFFSET, CENTER_Y_OFFSET)
center_b = (CENTER_X_OFFSET, CENTER_Y_OFFSET)
center_c = (0, -CENTER_Y_OFFSET)

# 三个圆的颜色 (低饱和)
low_saturation_colors = ('red', 'green', 'blue')

set_labels = ('Group A', 'Group B', 'Group C')
centers = [center_a, center_b, center_c]

# 子集数据
subsets = (10, 8, 22, 6, 9, 4, 2)

# --- 辅助函数：移动画笔并设置颜色 ---
def setup_turtle(x, y, color):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(color)

# --- 绘制三个圆的轮廓 ---
for center, color in zip(centers, low_saturation_colors):
    setup_turtle(center[0], center[1] - RADIUS, color)
    t.pensize(3)
    t.circle(RADIUS)

# --- 标注集合标签 (A, B, C) ---
LABEL_DIST = 120
label_offsets = [
    (-CENTER_X_OFFSET - 1.2*LABEL_DIST, CENTER_Y_OFFSET),  # Group A: 移到左侧更远
    (CENTER_X_OFFSET + 1.2*LABEL_DIST, CENTER_Y_OFFSET),   # Group B: 移到右侧更远
    (0, -CENTER_Y_OFFSET - 1.1*LABEL_DIST)                  # Group C: 移到下方更远
]

t.color('black')
t.pensize(1)
for label, offset in zip(set_labels, label_offsets):
    t.penup()
    t.goto(offset[0], offset[1])
    t.write(label, align="center", font=("Arial", 14, "bold"))


# --- 标注子集数字 ---
font_style = ("Arial", 10, "normal")

# 1. 仅 A (10)
setup_turtle(center_a[0] - RADIUS * 0.4, center_a[1] + RADIUS * 0.4, 'black')
t.write(subsets[0], align="center", font=font_style)

# 2. 仅 B (8)
setup_turtle(center_b[0] + RADIUS * 0.4, center_b[1] + RADIUS * 0.4, 'black')
t.write(subsets[1], align="center", font=font_style)

# 3. 仅 C (22)
setup_turtle(center_c[0], center_c[1] - RADIUS * 0.4, 'black')
t.write(subsets[2], align="center", font=font_style)

# 4. A ^ B (6) - A 和 B 的交集 (顶部)
setup_turtle(0, CENTER_Y_OFFSET + RADIUS * 0.25, 'black')
t.write(subsets[3], align="center", font=font_style)

# 5. A ^ C (9) - A 和 C 的交集 (左下)
setup_turtle(-CENTER_X_OFFSET * 0.5, -CENTER_Y_OFFSET * 0.5, 'black')
t.write(subsets[4], align="center", font=font_style)

# 6. B ^ C (4) - B 和 C 的交集 (右下)
setup_turtle(CENTER_X_OFFSET * 0.5, -CENTER_Y_OFFSET * 0.5, 'black')
t.write(subsets[5], align="center", font=font_style)

# 7. A ^ B ^ C (2) - 三者交集 (中心)
setup_turtle(0, 0, 'black')
t.write(subsets[6], align="center", font=font_style)

# 完成绘图，保持窗口打开
screen.mainloop()
