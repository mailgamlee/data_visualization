import numpy as np
import pandas as pd
from plotnine import *
from plotnine.data import mtcars

# mat_corr=np.round(mtcars.corr(),1).reset_index()
mat_corr = pd.DataFrame({'index': ['01', '02', '03', '04', '05'],
                             '01':[-0.3, -0.2, -0.1, 0.3, -0.4], 
                             '02':[-0.3, -0.2, -0.1, 0.3, -0.3],
                             '03':[-0.3, -0.2, -0.1, 0.3, -0.3],
                             '04':[-0.3, -0.2, -0.1, 0.3, -0.2],
                             '05':[-0.3, -0.2, -0.1, 0.2, -0.2]}) 
mydata=pd.melt(mat_corr,id_vars='index',var_name='var',value_name='value')
mydata['AbsValue']=np.abs(mydata.value)

#------------------------------------------------(b) 气泡图------------------------------------------
base_plot=(ggplot(mydata, aes(x ='index', y ='var', fill = 'value',size='AbsValue')) +  
  geom_point(shape='o',colour="black") +
  scale_size_area(max_size=11) +
  scale_fill_cmap(name ='RdYlBu_r')+
  coord_equal()+
    theme(dpi=100,figure_size=(4,4)))
# print(base_plot)
base_plot.show()

#------------------------------------------------(c) 方块图------------------------------------------------
base_plot=(ggplot(mydata, aes(x ='index', y ='var', fill = 'value',size='AbsValue')) +  
  geom_point(shape='s',colour="black") +
  scale_size_area(max_size=10) +
  scale_fill_cmap(name ='RdYlBu_r')+
  coord_equal()+
    theme(dpi=100, figure_size=(4,4)))
# print(base_plot)
base_plot.show()

# ------------------------------------------------(f) 带标签的热力图-----------------------------------
base_plot=(ggplot(mydata, aes(x ='index', y ='var', fill = 'value',label='value')) +
    geom_tile(colour="black") +
    geom_text(size=8,colour="white")+
    scale_fill_cmap(name ='RdYlBu_r')+
    coord_equal()+
        theme(dpi=100,figure_size=(4,4)))
# print(base_plot)
base_plot.show()

stop_here = 1
