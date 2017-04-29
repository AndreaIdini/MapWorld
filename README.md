## Description
Playing with maps, using GIS, fiona, Basemap, shapefiles.

## History
Map downloaded from https://borders.ukdataservice.ac.uk/, license in directory. England map divided by postal code region.
These maps are in OSGB coordinate reference system, that is NOT latitude and longitude, thus is not usable with the convenient Basemaps or any WGS84 continental map.
The most convenient conversion (precision of the conversion is down to ± few meters), is with ogr2ogr, from GDAL package.

Script ./Map/convert_OSGBtoWGS84.sh is setup accordingly.

## Author etc.
from Andrea Idini, drop me an email, you can find me ;)
