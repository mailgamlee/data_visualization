import matplotlib.pyplot as plt
from matplotlib import cm
from math import log10

labels = list("ABCDEFG")
data = [21, 57, 88, 14, 76, 91, 26]
# number of data points
n = len(data)
# find max value for full ring
k = 10 ** int(log10(max(data)))
m = k * (1 + max(data) // k)

# radius of donut chart
r = 1.5
# 计算每个扇区的宽度
w = r / n

# create colors along a chosen colormap
colors = [cm.terrain(i / n) for i in range(n)]  # cm.terrain()函数作用是返回一个颜色的序列，从红到绿到蓝。类似颜色序列的还有cm.rainbow()、cm.cool()等。

# create figure, axis
fig, ax = plt.subplots()
ax.axis("equal")

# create rings of donut chart
for i in range(n):
    # hide labels in segments with textprops: alpha = 0 - transparent, alpha = 1 - visible
    innerring, _ = ax.pie([m - data[i], data[i]], radius = r - i * w, startangle = 90, labels = ["", labels[i]], labeldistance = 1 - 1 / (1.5 * (n - i)), textprops = {"alpha": 0}, colors = ["white", colors[i]])
    plt.setp(innerring, width = w, edgecolor = "white")

plt.legend()
plt.show()
idebug = 1
