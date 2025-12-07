import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(subplot_kw=dict(aspect=1), facecolor='#232533')  # 定义子图，设置长宽比为1，背景色为黑色

# 外圈
theta = np.arange(-1 / 4 * np.pi, 5 / 4 * np.pi, 0.001)
x = np.cos(theta) * 1.2
y = np.sin(theta) * 1.2
ax.plot(x, y, c='#203360', alpha=0.5)

# 内圈
x = np.cos(theta) * 0.7
y = np.sin(theta) * 0.7
ax.plot(x, y, c='#203360', alpha=0.5)
# x = np.cos(theta2)
# y = np.sin(theta2)
# ax.plot(x, y, color='black')

# 绘制20%刻度
tick_theta = np.arange(-1 / 4 * np.pi, 5 / 4 * 1.1 * np.pi, 3 / 10 * np.pi)
point_x_on_circle = [np.cos(i) for i in tick_theta]
point_y_on_circle = [np.sin(i) for i in tick_theta]

tick_point_y = [18 / 20 * i for i in point_y_on_circle]
tick_point_x = [18 / 20 * i for i in point_x_on_circle]

label_point_y = [17 / 20 * i for i in point_y_on_circle]
label_point_x = [17 / 20 * i for i in point_x_on_circle]

for i in np.arange(len(tick_theta)):
    # 绘制20%刻度
    x = [tick_point_x[i], point_x_on_circle[i]]
    y = [tick_point_y[i], point_y_on_circle[i]]
    ax.plot(x, y, c='#1f3354', linewidth=7)
    ax.plot(x, y, c='#41b2f1')
    # 绘制20%刻度标签
    x = label_point_x[i]
    y = label_point_y[i] * 9 / 10
    ax.text(s=100 - i * 20, x=x, y=y, c='#629cd7', fontsize=10,
            horizontalalignment='center',
            verticalalignment='bottom')

# 绘制10%刻度
tick_theta = np.arange(-1 / 4 * np.pi, 5 / 4 * np.pi, 3 / 40 * np.pi)
point_x_on_circle = [np.cos(i) for i in tick_theta]
point_y_on_circle = [np.sin(i) for i in tick_theta]

point_y = [38 / 40 * i for i in point_y_on_circle]
point_x = [38 / 40 * i for i in point_x_on_circle]

for i in np.arange(len(tick_theta)):
    x = [point_x[i], point_x_on_circle[i]]
    y = [point_y[i], point_y_on_circle[i]]
    ax.plot(x, y, c='#41b2f1')

# 绘制圆心
heart_x = 0
heart_y = 0
ax.plot(heart_x, heart_y, 'o', color='#1e3b6c', markersize=14, alpha=.4)
ax.plot(heart_x, heart_y, 'bo', markersize=7)

# 计算箭头的位置
num = len(theta)
percent = 0.64
alpha_index = int((1 - percent) * num - 0.99999)
alpha = theta[alpha_index]
a_x = np.cos(alpha) * .7
a_y = np.sin(alpha) * .7
ax.annotate(text='', xy=(a_x, a_y), xytext=(-a_x * .15, -a_y * .15),
            arrowprops=dict(width=.3, headwidth=4, headlength=6, fc='#2863d5', ec='#2863d5'))

# 绘制结果标签,
ax.text(s=int(percent * 100),
        x=0,
        y=-0.6,
        fontsize=45,
        c='#274ab4',
        bbox=dict(boxstyle='round', fc='#274ab4', ec='#274ab4', alpha=0.1, pad=0.1),
        ha='center',
        va='top')
ax.axis('off')
plt.show()
idebug = 1
