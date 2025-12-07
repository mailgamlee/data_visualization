import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)
from matplotlib.cbook import get_sample_data

#中文及负号处理
plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False

N = 5
width = 0.55
x1 = np.array([1000, 500, 300, 200,150])
x2= np.array((x1.max()-x1)/2) # 占位
#x1+x2
x3=[]
for i,j in zip(x1,x2):
    x3.append(i+j)
x3 = np.array(x3)


y = -np.sort(-np.arange(N)) # 倒转y轴
labels=['浏览商品','放入购物车','生成订单','支付订单','完成交易']

#figure
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)

#plot
ax.barh(y,x3,width,tick_label=labels,color='r',alpha=0.85)
ax.plot(x3,y,'red',alpha=0.7)
ax.barh(y,x2,width,color='w',alpha =1) #辅助图
ax.plot(x2,y,'red',alpha=0.7)

#setting
transform = []       
for i in range(0,len(x1)):
    if i < len(x1)-1:
        transform.append('%.2f%%'%((x1[i+1]/x1[i])*100))
l = [(500,3),(500,2),(500, 1),(500, 0)]
for a,b in zip(transform,l):
    #offsetbox = TextArea(a, minimumdescent=False)
    offsetbox = TextArea(a)
    ab = AnnotationBbox(offsetbox, b,
                        xybox=(0, 40),
                        boxcoords="offset points",
                        arrowprops=dict(arrowstyle="->"))
    ax.add_artist(ab)
ax.set_xticks([0,1000])
ax.set_yticks(y)

plt.show()
idebug = 1