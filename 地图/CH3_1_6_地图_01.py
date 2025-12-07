import geopandas
import geoplot
from plotnine import *
'''
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))


#-----------------------------Methods:plotnine-----------------------------------------------
base_plot=(ggplot()+
           geom_map(world, aes(fill='gdp_md_est'))+
         #scale_fill_distiller(type='seq', palette='reds'))
         scale_fill_distiller(type='seq', palette='Reds'))
print(base_plot)
'''

#-------------------------Method:basemap---------------------------------------------------
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

ax = plt.figure(figsize=(8, 6)).gca()

basemap = Basemap(projection = 'cyl', lat_0 = 0, lon_0 = 0,resolution='l',ax=ax) 

#’ortho’指正射投影
#basemap = Basemap(projection = 'ortho', lat_0 = 0, lon_0 = 0,resolution='l',ax=ax) 

basemap.fillcontinents(color='orange',lake_color='#000000') 
basemap.drawcountries(linewidth=1,color='k')
basemap.drawcoastlines(linewidth=1,color='k')
basemap.drawparallels(np.arange(-90,90,30),labels=[1,0,0,0],zorder=0)
basemap.drawmeridians(np.arange(basemap.lonmin,basemap.lonmax+30,60),labels=[0,0,0,1],zorder=0)
plt.show()
test = 1