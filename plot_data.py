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
placeName="Guildford"

rangesList = scrape.search_Ranges_WorkBk(dataFlnm,placeName)
### -                CAREFUL, IT TAKES ALTO THE TOTALS

#print rangesList
dataFile = scrape.from_Rng_to_DataFrame(dataFlnm,rangesList)

df_map = mapDataPlot.mP_data(mapName,dataFile);

fig     = plt.figure()
ax      = fig.add_subplot(111)

ax.add_collection(PatchCollection(df_map['patches'].values,match_original=True))

ax.axis('auto')#; ax.axis('off')

plt.show()
