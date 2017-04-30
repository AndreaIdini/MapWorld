## Function to plot choropleth maps of data on top of shapefiles map ##
## A. Idini 2017 ##

#- function mP_Basemap takes in input filename and outputs patches for plotting -#
#- builds up a whole Basemap--based Panda dataframe with the list of patches,
#- and the corresponding wards names from shapefile
#- Input: flnm: string, filename path
#-        (optional)imp: Bool, if to import libraries
#- output: return to dataframe of
#-         ['patches'] Polygon patches
#-         ['properties'] patches properties
#-         ['area_m']  area in sq meters
#-         ['area_km'] area in sq km
#- ...
def mP_data(flnm, df, imp = None):
    if imp is None:
        import pandas as pd
        import matplotlib.pyplot as plt
        from mpl_toolkits.basemap import Basemap
        from shapely.geometry import Point, Polygon, MultiPoint, MultiPolygon
        from matplotlib.collections import PatchCollection
        from descartes import PolygonPatch
        import fiona
        from itertools import chain

    shp = fiona.open(flnm+'.shp')
    bds = shp.bounds
    extra = 0.02

    if 'units' in shp.crs and shp.crs['units'] == 'm':
        print 'Unit is meters, converting boundaries'
        conv = Basemap()
        ll = conv(bds[0],bds[1],inverse=True)
        ur = conv(bds[2],bds[3],inverse=True)
        print shp.crs
    else:
        ll = (bds[0], bds[1])
        ur = (bds[2], bds[3])

#    shp.close()
    coords = list(chain(ll, ur))

    w, h = coords[2] - coords[0], coords[3] - coords[1]
#    print coords; print extra

# Check proj4, .prj file...
    m = Basemap(
        projection='tmerc',
        lon_0=-2.,
        lat_0=49.,
        ellps = 'WGS84',
        llcrnrlon=coords[0] - extra * w,
        llcrnrlat=coords[1] - extra + 0.01 * h,
        urcrnrlon=coords[2] + extra * w,
        urcrnrlat=coords[3] + extra + 0.01 * h,
        lat_ts=0,
        resolution='i',
        suppress_ticks=True)

    m.readshapefile(
        flnm,
        'map',
        color='none',
        zorder=2)
    #
    # m.drawmapscale(
    #     coords[0] + 0.08, coords[1] + 0.015,
    #     coords[0], coords[1],
    #     10.,
    #     barstyle='fancy', labelstyle='simple',
    #     fillcolor1='w', fillcolor2='#555555',
    #     fontcolor='#555555',
    #     zorder=5)

    # set up a map dataframe

    temp_df = pd.DataFrame()

    for dicti in m.map_info:
        temp_df = temp_df.append(pd.Series(dicti),ignore_index=True)

    df_map = pd.DataFrame({'poly': [Polygon(xy) for xy in m.map]})

    df_map = pd.concat([df_map, temp_df], axis=1, join_axes=[df_map.index])

    df_map['area_m'] = df_map['poly'].map(lambda x: x.area)
    df_map['area_km'] = df_map['area_m'] / 10000.

    # draw ward patches from polygons
    df_map['patches'] = df_map['poly'].map(lambda x: PolygonPatch(
        x,
        fc='#555555',
        ec='#787878', lw=.75, alpha=.9,
        zorder=4))

    return df_map;