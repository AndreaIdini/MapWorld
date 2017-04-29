## Description
Playing with maps, using GIS, [fiona](http://toblerity.org/fiona/manual.html), Basemap, shapefiles.

# map.py
plot a geographical map, using functions in mapPlot.py

# scrape.py
 Scrape from Excel data tables finding intervals where string appears, in order to lookup postcode and data

## History and Datasets
Map downloaded from [UK borders data service](https://borders.ukdataservice.ac.uk/), license in directory. England map divided by postal code region.
These maps are in [OSGB coordinate reference system](https://en.wikipedia.org/wiki/Ordnance_Survey_National_Grid), that is NOT latitude and longitude, thus is not usable with the convenient Basemaps or any WGS84 continental map.
The most convenient conversion (precision of the conversion is down to ± few meters), is with ogr2ogr, from GDAL package.

Script ./Map/convert_OSGBtoWGS84.sh is setup accordingly, check .prj file for [Proj4 parameters](http://proj4.org/parameters.html) to verify setup

Pers_Mortage_PCS_2016-q3.xlsx of Mortage data [from cml.org.uk](https://www.cml.org.uk/industry-data/about-postcode-lending/)
SME and Personal Lending xlsx data tables [from bba.org.uk ](https://www.bba.org.uk/news/statistics/postcode-lending/borrowing-across-the-country-q3-2016/#.WQSIulPytAY)

## Author etc.
from Andrea Idini, drop me an email, you can find me ;)
License: GPL3.0
