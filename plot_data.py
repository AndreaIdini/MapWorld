import shapefile
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from descartes import PolygonPatch
import matplotlib
import numpy as np
import mapPlot
import scrape
#   -- plot --

mapName="./Map/england_pcs_2012_wgs84"
dataFile="Pers_Mortage_PCS_2016-q3.xlsx"
placeName="London"

rangesList = scrape.search_Ranges_WorkBk(dataFile,placeName)
print rangesList

#patches = mapPlot.mP(filename)
df_map = mapPlot.mP_Basemap(mapName); patches = df_map['patches']
#print df_map['properties']

fig     = plt.figure()
ax      = fig.add_subplot(111)

ax.add_collection(PatchCollection(patches,facecolor='0.75', edgecolor='w', linewidths=.2))

ax.axis('auto')#; ax.axis('off')

plt.show()
