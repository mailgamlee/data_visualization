import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# 中文字体设置
matplotlib.rcParams['font.family']='SimHei'
matplotlib.rcParams['font.sans-serif'] = ['SimHei']

labels = np.array(['综合', 'KDA', '发育', '推进', '生存','输出'])  # 定义标签数组，包含六个属性名称
nAttr = 6  # 定义属性的数量为6
data = np.array([7, 5, 6, 9, 8, 7])  # 数据值，这里是一个包含六个数值的数组
angles = np.linspace(0, 2*np.pi, nAttr, endpoint=False)  # 生成角度数组，从0到2π均匀分布的6个角度

data = np.concatenate((data, [data[0]]))  # 将数据数组的第一个元素添加到末尾，以便闭合雷达图
angles = np.concatenate((angles, [angles[0]]))  # 将角度数组的第一个元素添加到末尾，以便闭合雷达图

fig = plt.figure(facecolor="white")  # 创建一个背景为白色的图形
plt.subplot(111, polar=True)  # 添加一个极坐标子图，111表示1行1列的第一个子图
plt.plot(angles,data,'go-',linewidth=2)  # 绘制雷达图，'go-'表示绿色圆点和线条，线宽为2
plt.fill(angles,data,facecolor='g',alpha=0.25)  # 填充雷达图内部，绿色填充，透明度为0.25
plt.thetagrids(angles[0:6]*180/np.pi, labels)  # 设置角度网格标签，将角度转换为度数并对应标签
plt.figtext(0.52, 0.95, 'DOTA能力值雷达图', ha='center')  # 在图形的指定位置添加文本，这里是图形的顶部居中位置
plt.grid(True)  # 显示网格
plt.show()  # 显示图形
