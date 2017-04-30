import shapefile
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from descartes import PolygonPatch
import matplotlib
import numpy as np
import pandas as pd
import openpyxl as op

import mapDataPlot
import scrape
#   -- plot --

mapName="./Map/england_pcs_2012_wgs84"
#dataFile="Pers_Mortage_PCS_2016-q3.xlsx"
dataFlnm="test.xlsx"
placeName="London"

print 'Search ranges in ' + dataFlnm + ' ...'
rangesList = scrape.search_Ranges_WorkBk(dataFlnm,placeName)
### -                CAREFUL, IT TAKES ALTO THE TOTALS

print 'Building Dataframe from ' + dataFlnm + ' ...'
dataFile = scrape.from_Rng_to_DataFrame(dataFlnm,rangesList)

print 'Building map frame using ' + mapName + ' ...'
df_map = mapDataPlot.mP_data(mapName,dataFile);

fig     = plt.figure()
ax      = fig.add_subplot(111)

ax.add_collection(df_map)

print "axes and plotting!"

ax.axis('auto')#; ax.axis('off')

plt.show()
