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
import analyze
#   -- plot --

mapName   = "./Map/england_pcs_2012_wgs84"
dataFlnm="Pers_Mortage_PCS_2016-q3.xlsx"
#dataFlnm  = "SME_Lending_PCS_2016-q3.xlsx"
placeName = "London"
colName   = 'index'

print 'Search ranges in ' + dataFlnm + ' ...'
rangesList = scrape.search_Ranges_WorkBk(dataFlnm,placeName)
### -                CAREFUL, IT TAKES ALTO THE TOTALS

print 'Building Dataframe from ' + dataFlnm + ' ...'
dataFile = scrape.from_Rng_to_DataFrame(dataFlnm,rangesList)

print 'Analyzing market data...'
dataFile = analyze.add_Index_with_OLS(dataFile)

print 'Building map frame using ' + mapName + ' ...'

mapDataPlot.mP_data(mapName,colName,dataFile);
