#!bin/sh
echo "Please write filename to convert (no extension)"
read filename
echo "ogr2ogr -t_srs EPSG:4326 -s_srs "+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.999601 +x_0=400000 +y_0=-100000 +ellps=airy +units=m +no_defs +towgs84=375,-111,431" ${filename}_wgs84.shp ${filename}.shp" 
ogr2ogr -t_srs EPSG:4326 -s_srs "+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.999601 +x_0=400000 +y_0=-100000 +ellps=airy +units=m +no_defs +towgs84=375,-111,431" ${filename}_wgs84.shp ${filename}.shp 
echo "end, if error returned, check prj file correspondence with convertion parameters. These are setup to work with outputs from GB data service, setup might vary, use your brain."
