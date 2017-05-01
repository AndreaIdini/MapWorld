## Description
Playing with maps, using GIS, [fiona](http://toblerity.org/fiona/manual.html), Basemap, shapefiles.

# mapPlot.py
 Main program to plot data from .xlsx into map from shapefile.
 .xlsx will have a column of data, a column of keyword, and a column of postcodes.

 Calls **scrape.py** to select a range where a keyword appears, building a DataFrame with the data where keywords appears (e.g. London).
 Calls then **mapPlot.py** to plot from shapefile the area of same postcodes of .xlsx.

 Result is that if you write "London" you will have a map of all London districts of your data, divided by postcode. If you write Sheffield, a map of Sheffield...etc...

 NOTE: London area includes suburbs, such as Guildford. Results may not be as you are used to.
       Geographical mindblowing parental advisory explicit content.

# scrape.py
 Scrape from Excel data tables finding intervals where string appears, in order to lookup postcode and data, and building the corresponding dataframe for the given range. This dataframe will be used by **mapPlot.py** to plot data

# map.py
 Plot a basic geographical map, using functions in mapPlot.py, reading from a given shapefile.
 Usually works, especially if you use the mP function that is only patch--based.

## History and Datasets
Map downloaded from [UK borders data service](https://borders.ukdataservice.ac.uk/), license in directory. England map divided by postal code region.
These maps are in [OSGB coordinate reference system](https://en.wikipedia.org/wiki/Ordnance_Survey_National_Grid), that is NOT latitude and longitude, thus is not usable with the convenient Basemaps or any WGS84 continental map.
The most convenient conversion (precision of the conversion is down to ± few meters), is with ogr2ogr, from GDAL package.

Script ./Map/convert_OSGBtoWGS84.sh is setup accordingly, check .prj file for [Proj4 parameters](http://proj4.org/parameters.html) to verify setup

Pers_Mortage_PCS_2016-q3.xlsx of Mortage data [from cml.org.uk](https://www.cml.org.uk/industry-data/about-postcode-lending/)
SME and Personal Lending xlsx data tables [from bba.org.uk ](https://www.bba.org.uk/news/statistics/postcode-lending/borrowing-across-the-country-q3-2016/#.WQSIulPytAY)

## Inspiration and sources
Some functions and inspiration for the map plots taken from:
[Stephan Huegel](http://sensitivecities.com/so-youd-like-to-make-a-map-using-python-EN.html#.WQXrzVMrJAY)
[Ramiro Gomez](http://ramiro.org/notebook/basemap-choropleth/)
Various readthedocs.org pages, such as [openpyxl](http://openpyxl.readthedocs.io/en/default/tutorial.html)

## Author etc.
from Andrea Idini, drop me an email, you can find me ;)
License: GPL3.0
