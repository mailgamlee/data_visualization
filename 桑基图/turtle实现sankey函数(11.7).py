import turtle
import numpy as np

# 数据 (保持不变)
nodes = [
    [('Product', 20779), ('Sevice\nand other', 30949)],
    [('Total revenue', 51728)],
    [('Gross margin', 34768), ('Cost of revenue', 16960)],
    [('Operating income', 22247), ('Other income, net', 268), ('Research and\ndevelopment', 5758),
     ('Sales and marketing', 5379), ('General and\nadministrative', 1384)],
    [('Income before\nincome taxes', 22515)],
    [('Net income', 18765), ('Provision for\nincome taxes', 3750)]
]

# --- 颜色映射 (保持不变) ---
NODE_COLORS = {
    'Product': '#69a7d3',  # 蓝色
    'Sevice\nand other': '#ffbb78',  # 橙色
    'Total revenue': '#5cb85c',  # 绿色
    'Gross margin': '#d9534f',  # 红色
    'Cost of revenue': '#9467bd',  # 紫色
    'Operating income': '#8c564b',
    'Other income, net': '#9e9e9e',
    'Research and\ndevelopment': '#7f7f7f',
    'Sales and marketing': '#bcbd22',
    'General and\nadministrative': '#17becf',
    'Income before\nincome taxes': '#69a7d3',  # 沿用 Product 的蓝色
    'Net income': '#ffbb78',
    'Provision for\nincome taxes': '#98df8a',
}

# 流程数据 (修改：为指定的五个流向添加 'curve': True 标志)
flows = [
    # 直线流向 (默认)
    ('Product', 'Total revenue', 20779, {'flow_color_mode': 'dest', 'flow_override_color': NODE_COLORS['Product']}),
    ('Sevice\nand other', 'Total revenue', 30949,
     {'flow_color_mode': 'dest', 'flow_override_color': NODE_COLORS['Sevice\nand other']}),
    ('Total revenue', 'Gross margin', 34768, {'flow_color_mode': 'dest'}),
    ('Total revenue', 'Cost of revenue', 16960, {'flow_color_mode': 'dest'}),
    ('Gross margin', 'Operating income', 22247, {'flow_color_mode': 'dest'}),
    ('Operating income', 'Income before\nincome taxes', 22247, {'flow_color_mode': 'dest'}),
    ('Income before\nincome taxes', 'Net income', 18765, {'flow_color_mode': 'dest'}),  # Net income 仍是直线

    # 曲线流向 (新增 'curve': True)
    # 1. Gross margin 分流的三个
    ('Gross margin', 'Research and\ndevelopment', 5758, {'flow_color_mode': 'dest', 'curve': True}),
    ('Gross margin', 'Sales and marketing', 5379, {'flow_color_mode': 'dest', 'curve': True}),
    ('Gross margin', 'General and\nadministrative', 1384, {'flow_color_mode': 'dest', 'curve': True}),

    # 2. Other income, net 流入
    ('Other income, net', 'Income before\nincome taxes', 268,
     {'flow_color_mode': 'source', 'flow_override_color': '#e377c2', 'curve': True}),

    # 3. Provision for income taxes 流出
    ('Income before\nincome taxes', 'Provision for\nincome taxes', 3750, {'flow_color_mode': 'dest', 'curve': True}),
]

# --- 全局配置 (保持不变) ---
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
Y_DRAWING_HEIGHT = 500
X_START = -450
X_END = 450
NODE_WIDTH = 3
TEXT_OFFSET_X = 5
MAX_FLOW_VALUE = 51728.0
DARKEN_AMOUNT = 30
BORDER_PENSIZE = 3


# --- 辅助函数：颜色变暗 (保持不变) ---
def darken_color(hex_color, amount):
    """将十六进制颜色代码变暗指定量"""
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    r = max(0, rgb[0] - amount)
    g = max(0, rgb[1] - amount)
    b = max(0, rgb[2] - amount)
    return f'#{r:02x}{g:02x}{b:02x}'


def get_node_color(name):
    return NODE_COLORS.get(name, '#808080')


def get_flow_color(source_name, target_name, attrs):
    """获取流程颜色，并处理特殊颜色和模式"""
    if 'flow_override_color' in attrs:
        return attrs['flow_override_color']

    mode = attrs.get('flow_color_mode', 'source')

    if mode == 'dest':
        return get_node_color(target_name)
    else:
        return get_node_color(source_name)


def go_to(x, y):
    """移动海龟到指定坐标 (不画线)"""
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()


def setup_turtle_screen():
    """设置海龟绘图环境"""
    turtle.setup(width=SCREEN_WIDTH + 50, height=SCREEN_HEIGHT + 50)
    turtle.setworldcoordinates(-SCREEN_WIDTH / 2, -SCREEN_HEIGHT / 2, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    turtle.hideturtle()
    turtle.speed(0)
    turtle.colormode(255)


def pre_process_data_turtle(nodes):
    """预计算所有节点的位置和流量点"""
    node_map = {}
    num_levels = len(nodes)
    x_coords = np.linspace(X_START, X_END - NODE_WIDTH, num_levels)

    for level_index, level_nodes in enumerate(nodes):
        x = x_coords[level_index]
        current_y_top = Y_DRAWING_HEIGHT / 2.0

        for name, value_ in level_nodes:
            height = (value_ / MAX_FLOW_VALUE) * Y_DRAWING_HEIGHT
            y_bottom = current_y_top - height

            node_map[name] = {
                'x_left': x,
                'x_right': x + NODE_WIDTH,
                'y_top': current_y_top,
                'y_bottom': y_bottom,
                'height': height,
                'value': value_,
                'color': get_node_color(name),
                'out_current_y': current_y_top,
                'in_current_y': current_y_top,
                'level': level_index,
            }

            current_y_top = y_bottom

    return node_map


NODE_POSITIONS_TURTLE = pre_process_data_turtle(nodes)


def draw_node_rectangle(x, y_bottom, width, height, color, name):
    """
    绘制节点矩形及其边框。
    """
    dark_color = darken_color(color, DARKEN_AMOUNT)

    go_to(x, y_bottom)

    if name == 'Total revenue':
        turtle.fillcolor('white')
        turtle.pencolor(dark_color)
        turtle.pensize(BORDER_PENSIZE)
    else:
        turtle.fillcolor(color)
        turtle.pencolor(dark_color)
        turtle.pensize(BORDER_PENSIZE)

    turtle.begin_fill()
    turtle.setheading(0)
    turtle.forward(width)
    turtle.left(90)
    turtle.forward(height)
    turtle.left(90)
    turtle.forward(width)
    turtle.left(90)
    turtle.forward(height)

    turtle.end_fill()


def create_node(name, color, value):
    """
    绘制节点矩形及其标签。
    """
    node_info = NODE_POSITIONS_TURTLE.get(name)
    if not node_info:
        return

    x = node_info['x_left']
    y_bottom = node_info['y_bottom']
    height = node_info['height']
    level = node_info['level']

    # 1. 绘制节点矩形
    draw_node_rectangle(x, y_bottom, NODE_WIDTH, height, color, name)

    # 2. 绘制标签和值
    y_center = y_bottom + height / 2
    lines = name.split('\n')
    turtle.pencolor('black')

    # 默认定位逻辑
    text_x = x + NODE_WIDTH + TEXT_OFFSET_X
    align = "left"

    if level == 0:
        text_x = X_START - TEXT_OFFSET_X
        align = "right"
    elif level == len(nodes) - 1:
        text_x = X_END + NODE_WIDTH + TEXT_OFFSET_X
        align = "left"
    elif level == 3:
        if name == 'Other income, net':
            rd_top_y = NODE_POSITIONS_TURTLE.get('Research and\ndevelopment')['y_top']
            y_center = rd_top_y + 15
            text_x = x + NODE_WIDTH + TEXT_OFFSET_X + 15
            align = "left"
        elif name == 'Research and\ndevelopment':
            y_center = y_bottom + height - 20
            text_x = x + NODE_WIDTH + TEXT_OFFSET_X
            align = "left"
        elif name == 'General and\nadministrative':
            y_center = y_bottom + height / 2 + 5
            text_x = x + NODE_WIDTH + TEXT_OFFSET_X
            align = "left"
        elif name == 'Operating income':
            y_center = y_bottom + height / 2 + 5
            text_x = x + NODE_WIDTH + TEXT_OFFSET_X
            align = "left"

    elif level == 1 or level == 2 or level == 4:
        y_center = y_bottom + height / 2 - 10

    # 写入标签 (字体大小为 11)
    if len(lines) == 1:
        go_to(text_x, y_center + 5)
        turtle.write(f"{name}", align=align, font=("Arial", 11, "normal"))
        go_to(text_x, y_center - 10)
        turtle.write(f"{value:,}", align=align, font=("Arial", 11, "normal"))
    else:
        y_start = y_center + 10

        go_to(text_x, y_start)
        turtle.write(f"{lines[0]}", align=align, font=("Arial", 11, "normal"))
        go_to(text_x, y_start - 12)
        turtle.write(f"{lines[1]}", align=align, font=("Arial", 11, "normal"))
        go_to(text_x, y_start - 27)
        turtle.write(f"{value:,}", align=align, font=("Arial", 11, "normal"))


def draw_bezier_curve(p0, p1, p2, num_steps=20):
    """绘制二次贝塞尔曲线的路径点"""
    path = []
    for i in range(num_steps + 1):
        t = i / num_steps
        # 二次贝塞尔公式: B(t) = (1-t)^2 * P0 + 2*(1-t)*t * P1 + t^2 * P2
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        path.append((x, y))
    return path


def draw_curve_flow(x1_start, y1_top, x2_start, y2_top, width, color):
    """绘制曲线流程，只保留左右粗边框"""
    dark_color = darken_color(color, DARKEN_AMOUNT)

    # 定义流程的四个关键点
    P1 = (x1_start, y1_top)
    P4 = (x1_start, y1_top - width)
    P2 = (x2_start, y2_top)
    P3 = (x2_start, y2_top - width)

    # 控制点 (使用中间点的 X 坐标，Y 保持在起点/终点的 Y)
    mid_x = x1_start + (x2_start - x1_start) * 0.5

    C1_top = (mid_x, P1[1])
    C2_top = (mid_x, P2[1])
    C1_bottom = (mid_x, P4[1])
    C2_bottom = (mid_x, P3[1])

    # 1. 计算贝塞尔曲线路径
    # 上边缘：P1 -> P2
    path_top = draw_bezier_curve(P1, C1_top, P2)
    # 下边缘：P4 -> P3
    path_bottom = draw_bezier_curve(P4, C1_bottom, P3)

    # 2. 绘制流程填充 (无粗边框)
    turtle.fillcolor(color)
    turtle.pencolor(color)  # 确保边界线与填充色相同，视觉上无边界
    turtle.pensize(1)

    go_to(path_top[0][0], path_top[0][1])
    turtle.begin_fill()

    # 绘制上边缘
    for x, y in path_top:
        turtle.goto(x, y)

    # 绘制右侧边框的连接线 (P2 到 P3)
    turtle.goto(P3[0], P3[1])

    # 绘制下边缘 (反向)
    for x, y in reversed(path_bottom):
        turtle.goto(x, y)

    # 闭合 (P4 到 P1)
    turtle.goto(P1[0], P1[1])

    turtle.end_fill()

    # 3. 单独绘制流量左右的粗边框 (与节点衔接处)
    turtle.pencolor(dark_color)
    turtle.pensize(BORDER_PENSIZE)

    # 绘制左侧边框 (源节点右侧)
    go_to(P1[0], P1[1])
    turtle.setheading(270)
    turtle.forward(width)

    # 绘制右侧边框 (目标节点左侧)
    go_to(P2[0], P2[1])
    turtle.setheading(270)
    turtle.forward(width)


def draw_straight_flow(x1_start, y1_top, x2_start, y2_top, width, color):
    """绘制简化直连流程，只保留左右粗边框"""
    dark_color = darken_color(color, DARKEN_AMOUNT)

    # 定义四个顶点
    P1 = (x1_start, y1_top)
    P4 = (x1_start, y1_top - width)
    P2 = (x2_start, y2_top)
    P3 = (x2_start, y2_top - width)

    # 流程中间的 X 坐标 (用于连接)
    mid_x = x1_start + (x2_start - x1_start) * 0.5

    C1_top = (mid_x, y1_top)
    C2_top = (mid_x, y2_top)
    C1_bottom = (mid_x, y1_top - width)
    C2_bottom = (mid_x, y2_top - width)

    # 1. 绘制流程填充 (无粗边框)
    turtle.fillcolor(color)
    turtle.pencolor(color)
    turtle.pensize(1)

    go_to(P1[0], P1[1])
    turtle.begin_fill()

    # 绘制上边缘
    turtle.goto(C1_top[0], C1_top[1])
    turtle.goto(C2_top[0], C2_top[1])
    turtle.goto(P2[0], P2[1])

    # 到目标节点下边缘
    turtle.goto(P3[0], P3[1])

    # 绘制下边缘 (反向)
    turtle.goto(C2_bottom[0], C2_bottom[1])
    turtle.goto(C1_bottom[0], C1_bottom[1])
    turtle.goto(P4[0], P4[1])

    # 4. 闭合
    turtle.goto(P1[0], P1[1])

    turtle.end_fill()

    # 2. 单独绘制流量左右的粗边框 (与节点衔接处)
    turtle.pencolor(dark_color)
    turtle.pensize(BORDER_PENSIZE)

    # 绘制左侧边框 (源节点右侧)
    go_to(P1[0], P1[1])
    turtle.setheading(270)
    turtle.forward(width)

    # 绘制右侧边框 (目标节点左侧)
    go_to(P2[0], P2[1])
    turtle.setheading(270)
    turtle.forward(width)


def draw_flow(x1_start, y1_top, x2_start, y2_top, width, color, is_curve):
    """根据 is_curve 参数选择绘制曲线或直线流向"""
    if is_curve:
        draw_curve_flow(x1_start, y1_top, x2_start, y2_top, width, color)
    else:
        draw_straight_flow(x1_start, y1_top, x2_start, y2_top, width, color)


def sankey_plot(flows):
    """主绘图函数，负责协调节点和流程的绘制。"""

    setup_turtle_screen()
    turtle.title("Sankey 仿制图 (曲线流向)")
    turtle.tracer(0, 0)

    node_data = NODE_POSITIONS_TURTLE

    # 重置 current_y
    for name in node_data:
        node_data[name]['out_current_y'] = node_data[name]['y_top']
        node_data[name]['in_current_y'] = node_data[name]['y_top']

    # 1. 先绘制流程，让其在底层
    for flow_tuple in flows:

        source_name, target_name, value, attrs = flow_tuple if len(flow_tuple) == 4 else flow_tuple + ({},)

        source = node_data.get(source_name)
        target = node_data.get(target_name)

        if not source or not target:
            continue

        flow_width = (value / MAX_FLOW_VALUE) * Y_DRAWING_HEIGHT
        flow_color = get_flow_color(source_name, target_name, attrs)

        # 确定是否需要绘制曲线
        is_curve = attrs.get('curve', False)

        # 这里的 X 坐标确保了流程从节点的外部边界开始/结束
        y1_top = source['out_current_y']
        x1_start = source['x_right']
        y2_top = target['in_current_y']
        x2_start = target['x_left']

        draw_flow(
            x1_start=x1_start,
            y1_top=y1_top,
            x2_start=x2_start,
            y2_top=y2_top,
            width=flow_width,
            color=flow_color,
            is_curve=is_curve  # 传入是否为曲线的标志
        )

        source['out_current_y'] -= flow_width
        target['in_current_y'] -= flow_width

    # 2. 后绘制节点及其标签，确保它们在最上层
    for name, data in node_data.items():
        create_node(name, data['color'], data['value'])

    # 3. 完成绘制
    turtle.update()
    turtle.mainloop()


# --- 运行绘图函数 ---
sankey_plot(flows)
