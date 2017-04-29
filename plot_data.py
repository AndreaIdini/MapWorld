import shapefile
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from descartes import PolygonPatch
import matplotlib
#import numpy as np
import pandas as pd
import openpyxl as op

import mapPlot
import scrape
#   -- plot --

mapName="./Map/england_pcs_2012_wgs84"
#dataFile="Pers_Mortage_PCS_2016-q3.xlsx"
dataFile="test.xlsx"
placeName="London"

rangesList=[(1247, 1283), (1285, 1339), (1341, 1616), (1618, 1751), (1753, 1810), (1812, 1847), (1849, 1938), (1940, 2203), (2205, 2511), (2513, 2541), (2543, 2621), (2623, 2675), (2677, 2863)]

#rangesList = scrape.search_Ranges_WorkBk(dataFile,placeName)
#print rangesList

scrape.from_Rng_to_DataFrame(dataFile,rangesList)
quit()


#patches = mapPlot.mP(filename)
df_map = mapPlot.mP_Basemap(mapName); patches = df_map['patches']
#print df_map['properties']

fig     = plt.figure()
ax      = fig.add_subplot(111)

ax.add_collection(PatchCollection(patches,facecolor='0.75', edgecolor='w', linewidths=.2))

ax.axis('auto')#; ax.axis('off')

plt.show()
