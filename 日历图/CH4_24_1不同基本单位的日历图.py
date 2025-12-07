import pandas as pd
import numpy as np
from plotnine import *

import matplotlib.pyplot as plt 

import calmap

df=pd.read_csv('Calendar.csv',parse_dates=['date'])  # read_csv(data, parse_dates=[column_name])参数指定日期列
df.set_index('date', inplace=True)  # 设置日期列为索引

fig,ax=calmap.calendarplot(df['value'],
                           fillcolor='grey',
                           linecolor='w',
                           linewidth=0.1,
                           cmap='RdYlGn',
                           yearlabel_kws={'color':'black', 'fontsize':12},
                           fig_kws=dict(figsize=(10,5),dpi=80))

fig.colorbar(ax[0].get_children()[1], ax=ax.ravel().tolist())

plt.show()
#fig.savefig('日历图1.pdf')
stop_here = 1