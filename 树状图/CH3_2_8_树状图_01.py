from matplotlib import pyplot as plt
from collections import defaultdict
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

# 核心函数
def plotTree(root: int, edges: list[list[int]], nodeGroups=[], groupLabels: list[str] = [], figureTitle="",
             labelOffset=0, heightDiff=5, fatherNodePosAdjustProportion=0.5, plotFormIdx=0, fieldAngle=180) -> None:
    """
    固定参数：
        root，根结点，dfs的起始点，必须要有
        edges=[[a,b],[a2,b2],...]，结点之间的无向边，在程序中会从根节点root遍历，来判断a、b哪个是父节点
    可选参数
        nodeGroups 将结点分组，不同的结点绘制不同的颜色
        groupLabels 是对每组结点的说明
        figureTitle 是图像标题
        labelOffset 是相邻叶子结点的间距，必须是正数，否则数字会混在一起
        heightDiff 是不同层间的距离，必须是非0数，支持正负数来调整树的朝向
        fatherNodePosAdjustProportion调整父结点的x位置，值为0.5时效果为居中
        plotFormIdx是指显示形式，目前支持三种，012分别是二叉树形式、目录树形式、扇形图形式
        fieldAngle 用于扇形图，接收角度形式的张角度数
    注意事项：
        edges中有环时，程序会根据遍历顺序打断环中最后一个遍历到的边，造成显示结果不稳定
        很早结束的分支仍然在后边的层中占据着空位
    """
    if len(nodeGroups) < 1:
        nodeGroups = [i for j in edges for i in j]
        nodeGroups = [list(set(nodeGroups))]
    elif 'list' not in str(type(nodeGroups[0])):
        nodeGroups = [nodeGroups]  # 统一改成多层数组
    if len(groupLabels) < len(nodeGroups):
        groupLabels += [f"第{i + 1}类" for i in range(len(groupLabels), len(nodeGroups))]
    if heightDiff == 0:
        print('高度朝向设置有问题，已初始化为1')
        heightDiff = 1
    childrens, ringEdges = getTreeAndRingEdgeFromGraph(root, edges)
    depth = depthOfTree(root, childrens)
    figureTitle += f"，深度：{depth}，结点数量：{nodeNumsOfTree(nodeGroups)}"
    plotFormIdx = int(plotFormIdx) % 3
    if plotFormIdx == 0:
        pos, labelPos = binaryTreeForm(root, childrens, heightDiff, fatherNodePosAdjustProportion, labelOffset)
    elif plotFormIdx == 1:
        pos, labelPos = ContentForm(root, childrens, heightDiff, fatherNodePosAdjustProportion)
    else:
        pos, labelPos = roundForm(root, childrens, heightDiff, fatherNodePosAdjustProportion, fieldAngle=fieldAngle)
    """
    三种模式要求的参数有区别
    二叉树模式需要父结点偏离比例、高度朝向，备选：标签x轴额外偏离值，用于
    目录模式  需要父结点偏离比例、高度朝向，备选：连线前置，改成两段，但会影响画图，暂时放弃
    扇形模式  需要父结点偏离比例、高度朝向、总角度
    """
    edges = [[a, b] for a in childrens for b in childrens[a]]
    for a, b in edges:
        if plotFormIdx != 1:
            line = [pos[a], pos[b]]
        else:
            if b != childrens[a][0]:
                line = [pos[childrens[a][0]], pos[b]]
            else:
                line = [pos[a], [pos[b][0], pos[a][1]]]
        line = list(zip(*line))
        if plotFormIdx != 1:  # 对应二叉树结构和扇形图结构，标签和边可能有交叉
            plt.plot(*line, color="lightgray")
        else:
            plt.plot(*line, color="gray")
    for idx, nodes in enumerate(nodeGroups):  # 绘制结点
        if len(nodes) == 0:
            continue
        points = [pos[i] for i in nodes]
        points = list(zip(*points))
        plt.scatter(*points, marker='o', label=groupLabels[idx])
    for i in labelPos:
        x, y = labelPos[i]
        plt.text(x, y, str(i))  # 数字

    if plotFormIdx == 1:  # 标签显示不完整，在最右边增加一个点
        rx, ry = labelPos[root]
        for i in labelPos:
            rx = max(rx, labelPos[i][0] + len(str(i)) / 2)
        bgc = plt.rcParams['axes.facecolor']
        plt.scatter([rx], [ry], c=bgc)

    for a, b in ringEdges:
        line = [pos[a], pos[b]]
        line = list(zip(*line))
        plt.plot(*line, linestyle=":", color='orange')

    plt.subplots_adjust(left=0, bottom=0, right=0.95, top=0.95)  # 右侧给标签数字留点空间
    plt.axis('off')
    plt.legend()
    plt.title(figureTitle)
    plt.show()


def binaryTreeForm(root, childrens, heightDiff=1, fatherNodePosAdjustProportion=0.5, labelOffset=0):
    """
    输出二叉树形式的结点位置坐标，每层结点的高度相同
    先自下而上获得每棵子树的宽度，再自上而下设置具体位置
    labelOffset：额外按数字长度比例地偏移标签位置
    """
    width = {}  # 每个结点代表的子树的宽度
    visited = {}

    def dfsGetWidth(node):
        if node in visited:
            print(f"存在环:{node}，已忽略")
            return 0
        visited[node] = True
        res = 0  # 不考虑空格了。图像放大，自然会出现空格
        for i in childrens[node]:
            res += dfsGetWidth(i)
        res = max(res, len(str(node)))  # 考虑数字长度，消除数字过长造成的重叠问题
        width[node] = res
        return res

    dfsGetWidth(root)

    pos = {}  # 存储每个结点的绘制坐标
    visited = {}

    def dfsGetPos(node, x0, y0):
        if node in visited:
            return
        visited[node] = True
        pos[node] = [x0 + width[node] * fatherNodePosAdjustProportion, y0]
        x = x0
        for i in childrens[node]:
            dfsGetPos(i, x, y0 + heightDiff)
            x += width[i]

    dfsGetPos(root, 0, 0)
    labelPos = {}
    for i in pos:
        x, y = pos[i]
        labelOffsetProportion = max(0, fatherNodePosAdjustProportion)
        labelOffsetProportion = min(1, labelOffsetProportion)  # 限制到0、1之间
        labelOffsetProportion *= -0.8
        labelOffsetProportion += labelOffset  # 用来比例补偿，线性补偿是把所有结点整体平移，无用
        x += labelOffsetProportion * len(str(i))  # 尽量使标记居中
        y += abs(heightDiff) / 6
        labelPos[i] = [x, y]
    return pos, labelPos


def ContentForm(root, childrens, heightDiff=1, fatherNodePosAdjustProportion=0):
    """
    获得树中结点的目录树格式的坐标，横向获得每层的数字的最大宽度
    """
    maxLen = []
    visited = {}

    def dfsGetMaxLengthOfEachLevel(node, curlevel=1):
        if node in visited:
            print(f"存在环:{node}，已忽略")
            return
        visited[node] = True
        if len(maxLen) < curlevel:
            maxLen.append(len(str(node)))
        elif len(str(node)) > maxLen[curlevel - 1]:
            maxLen[curlevel - 1] = len(str(node))
        for i in childrens[node]:
            dfsGetMaxLengthOfEachLevel(i, curlevel + 1)

    dfsGetMaxLengthOfEachLevel(root, 1)
    """
    先自下而上获得每棵子树的高度，再自上而下设置具体位置
    """
    height = {}  # 每个结点代表的子树的宽度
    visited = {}

    def dfsGetHeight(node):
        if node in visited:
            return 0
        visited[node] = True
        res = 0
        for i in childrens[node]:
            res += dfsGetHeight(i)
        if res == 0:
            res = heightDiff
        height[node] = res
        return res

    dfsGetHeight(root)

    pos = {}  # 存储每个结点的绘制坐标
    visited = {}

    def dfsGetPos(node, x0, y0, curlevel=1):
        if node in visited:
            return
        visited[node] = True
        pos[node] = [x0, y0 + fatherNodePosAdjustProportion * height[node]]
        x = x0 + maxLen[curlevel - 1]
        y = y0
        for i in childrens[node]:
            dfsGetPos(i, x, y, curlevel + 1)
            y += height[i]

    dfsGetPos(root, 0, 0)
    return pos, pos


def roundForm(root: int, childrens: dict[list[int]], heightDiff=1, fatherNodePosAdjustProportion=0.5, fieldAngle=120):
    """
    绘制扇形图，输出扇形图结点的位置和标签的位置
    fieldAngle：扇形图的张角，以角度制形式输入
    heightDiff,扇形图朝向，上或下
    fatherNodePosAdjustProportion，树的父结点居中偏移比例；
    """
    from math import sin, cos, pi
    fieldAngle = (fieldAngle / 2) * pi / 180
    radian = {}  # 效果等同于width

    def dfsGetRadian(node, level):  # 不同层级的radian要按比例收缩,level相当于半径
        res = 0
        for i in childrens[node]:
            dfsGetRadian(i, level + 1)
            res += radian[i]
        res = max(res * level / (level + 1), 1)
        radian[node] = res
        return res

    dfsGetRadian(root, 0)  # 根结点不占宽度
    pos = {}

    def dfsGetPos(node, level, angleStart, angleEnd):
        angle = angleStart * (1 - fatherNodePosAdjustProportion) + angleEnd * fatherNodePosAdjustProportion
        pos[node] = [level * cos(angle), level * sin(angle)]  # 扇心位于原点，直接用三角函数求坐标
        if radian[node] and level:
            radian[node] *= (level + 1) / level
        else:
            radian[node] = sum(radian[i] for i in childrens[node])
        angle = angleEnd - angleStart
        for i in childrens[node]:
            angleEnd = angleStart + angle * radian[i] / radian[node]
            dfsGetPos(i, level + 1, angleStart, angleEnd)
            angleStart = angleEnd

    if heightDiff > 0:
        angleSt, angleEd = pi / 2 + fieldAngle, pi / 2 - fieldAngle  # 保证从左向右
    else:
        angleSt, angleEd = 3 * pi / 2 - fieldAngle, 3 * pi / 2 + fieldAngle
    dfsGetPos(root, 0, angleSt, angleEd)
    return pos, pos


def nodeNumsOfTree(nodeGroups):
    """
    计算树中的结点数量
    """
    if 'list' not in str(type(nodeGroups[0])):
        return len(set(nodeGroups))
    res = set([])
    for i in nodeGroups:
        res |= set(i)
    return len(res)


#def depthOfTree(root: int, childrens: dict[list[int]] | list[list[int]]):
def depthOfTree(root: int, childrens: dict[list[int]] ):

    """
    计算树的深度，dfs
    """
    visited = {}

    def dfs(node):
        if node in visited:
            print(f"存在环:{node}，已忽略")
            return 0
        visited[node] = True
        res = 0
        for i in childrens[node]:
            res = max(res, dfs(i))
        return res + 1

    depth = dfs(root)
    return depth


def getTreeAndRingEdgeFromGraph(root: int, edges: list[list[int]]) -> tuple[dict[list[int]], list[list[int]]]:
    """
    去除图中的环，并输出环用以后续。方法为从根结点root开始bfs，消除环中反向的那一条边
    输出childrens，而非edges
    不管输入的neighbers是树还是多个不连接的图，都只检测root所在的那个树/图
    """
    edges0 = [tuple(sorted(i)) for i in edges]
    dc = {}
    edges = []
    for i in edges0:
        if i not in dc:
            dc[i] = 1
            edges.append(i)
    dc.clear()
    neighbers = defaultdict(list)
    for a, b in edges:
        neighbers[a].append(b)
        neighbers[b].append(a)

    childrens = defaultdict(list)
    ringsEdge = []  # 从环中去掉的边
    curNodes = [root]
    visited = {}
    level = 1
    while len(curNodes):
        nextNodes = []
        for i in curNodes:
            visited[i] = level
            for j in neighbers[i]:
                if j in visited:
                    if visited[j] != visited[i] - 1:
                        ringsEdge.append([i, j])
                else:
                    childrens[i].append(j)
                    nextNodes.append(j)
        curNodes = nextNodes
        level += 1
    return childrens, ringsEdge


# 例子，绘制冰雹猜想的3x+1树
def plot3xAdd1Tree(level=10):
    edges = []
    curNode = [1]
    nodes = [1]
    for i in range(1, level):
        newNode = [2 * j for j in curNode]
        newNode += [(j - 1) // 3 for j in curNode if j % 6 == 4 and j > 4]  # j是模3余1的偶数
        edges += [[j, (j - 1) // 3] for j in curNode if j % 6 == 4 and j > 4]
        edges += [[j, 2 * j] for j in curNode]
        curNode = newNode
        nodes += curNode
    nodes = [[i for i in nodes if i & 1], [i for i in nodes if i & 1 == 0]]
    nodeLabel = ["奇数", "偶数"]
    for i in range(3):  # 3种显示形式各画一次
        plotTree(1, edges, nodes, figureTitle="3x+1树", groupLabels=nodeLabel, heightDiff=-1, plotFormIdx=i,
                 fatherNodePosAdjustProportion=0.5)


if __name__ == "__main__":
    plot3xAdd1Tree(15)

idebug = 1