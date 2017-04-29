## General functions to plot shapefiles ##
## A. Idini 2017 ##

#- function mapPlot takes in input filename and outputs patches for plotting -#
#- builds up polygon patches reading the list of patches from shapefile
#- Input: flnm: string, filename path.
#-        (optional)imp: Bool, if to import libraries
#- output: return Polygon patches...
def mP(flnm, imp = None):
    if imp is None:
        import shapefile
        from matplotlib.patches import Polygon
        import matplotlib
        import numpy as np

    #   -- input --
    sf = shapefile.Reader(flnm)
    recs    = sf.records()
    shapes  = sf.shapes()
    Nshp    = len(shapes)
    cns     = []

    for nshp in xrange(Nshp):
        cns.append(recs[nshp][1])

    cns = np.array(cns)
    cm = matplotlib.cm.get_cmap('Dark2')
    cccol = cm(1.*np.arange(Nshp)/Nshp)

    #--- PatchBuild ---#
    ptchs   = []
    for nshp in xrange(Nshp):
        pts     = np.array(shapes[nshp].points)
        prt     = shapes[nshp].parts
        par     = list(prt) + [pts.shape[0]]

        for pij in xrange(len(prt)):
           ptchs.append(Polygon(pts[par[pij]:par[pij+1]]))

    return ptchs;


#- function mP_Basemap takes in input filename and outputs patches for plotting -#
#- builds up a whole Basemap--based Panda dataframe with the list of patches,
#- and the corresponding wards names from shapefile
#- Input: flnm: string, filename path
#-        (optional)imp: Bool, if to import libraries
#- output: return to dataframe of
#-         ['patches'] Polygon patches
#-         ['ward_name'] patches name
#-         ['area_m']  area in sq meters
#-         ['area_km'] area in sq km
#- ...
def mP_Basemap(flnm, imp = None):
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

    #coords [:] = [x/20000. for x in coords]
    w, h = coords[2] - coords[0], coords[3] - coords[1]
    print coords; print extra

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

    #print m.map_info

    # set up a map dataframe
    df_map = pd.DataFrame({
        'poly': [Polygon(xy) for xy in m.map]
        ,'properties': [ward['name'] for ward in m.map_info]
        })
    df_map['area_m'] = df_map['poly'].map(lambda x: x.area)
    df_map['area_km'] = df_map['area_m'] / 100000

    # draw ward patches from polygons
    df_map['patches'] = df_map['poly'].map(lambda x: PolygonPatch(
        x,
        fc='#555555',
        ec='#787878', lw=.75, alpha=.9,
        zorder=4))

    return df_map;
