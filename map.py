import shapefile
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from descartes import PolygonPatch
import matplotlib
import numpy as np
import mapPlot

#   -- plot --

filename="./Map/england_pcs_2012"


#patches = mapPlot.mP(filename)
df_map = mapPlot.mP_Basemap(filename); patches = df_map['patches']

#print df_map['ward_name']

fig     = plt.figure()
ax      = fig.add_subplot(111)

ax.add_collection(PatchCollection(patches,facecolor='0.75', edgecolor='w', linewidths=.2))

ax.axis('auto')#; ax.axis('off')

plt.show()
