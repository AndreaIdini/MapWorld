#######################################################################
## Function to plot choropleth maps of data on top of shapefiles map ##
##                         A. Idini 2017                             ##
#######################################################################
import numpy as np
import matplotlib
from mpl_toolkits.basemap import Basemap

#- function mP_data takes in input filename and datafile outputs patches for plotting -#
#- builds up a whole Basemap--based Panda dataframe with the list of patches,
#- and the corresponding wards names from shapefile and datafile
#- Input: flnm: string, filename path
#-        (optional)imp: Bool, if to import libraries
#- output: return to dataframe of
#-         ['patches'] Polygon patches
#-         ['properties'] patches properties
#-         ['area_m']  area in sq meters
#-         ['area_km'] area in sq km
#- ...
def mP_data(flnm, colName, df, imp = None):
    num_colors = 10

    if imp is None:
        import pandas as pd
        import matplotlib.pyplot as plt
        import matplotlib.colors as colors
        from shapely.geometry import Point, Polygon, MultiPoint, MultiPolygon
        from pysal.esda.mapclassify import Natural_Breaks as nb
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
        suppress_ticks=False)

    m.readshapefile(
        flnm,
        'map',
        color='none',
        zorder=2)

# Setup a dataframe that imports the dictionary of map properties and then
# selects rows corresponding to the imported dataframe df
    temp_df = pd.DataFrame()

    for dicti in m.map_info:
        temp_df = temp_df.append(pd.Series(dicti),ignore_index=True)
#    print temp_df; quit()

    i1 = temp_df.set_index('label').index
    i2 = df.set_index('Sector').index

    temp_df = temp_df[i1.isin(i2)]

    # set up a map dataframe
    df_map = pd.DataFrame({'poly': [Polygon(xy) for xy in m.map]})

    df_map['area_m'] = df_map['poly'].map(lambda x: x.area)

#Select only the part that corresonds to the imported dataframe of data
    df_map = pd.concat([df_map, temp_df], axis=1, join='inner')

    df_map['area_km'] = df_map['area_m'] / 10000.

    if len(df_map.index) == len(df.index):
        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
        print '!! WARNING : SHAPE OF DATAFRAMES NOT CONSISTENT !!'
        print '!! --- check: df_map  and df in mapDataPlot --- !!'
        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'

# Merge dataframes
    df_map = pd.merge(left=df_map, right=df, left_on='label', right_on='Sector',
                      how='inner')

    print '... built map frame ...'
## Calculates Jenks natural breaks, over notnull column

    prices = df_map[df_map[colName].notnull()][colName].tolist()

    breaks = nb ( prices,
        initial=250, #number of initial solutions in iteriative Jenks algo
        k=num_colors )

    print 'Calculting Jenks Natural breaks for binning'
    jenbin = pd.DataFrame({'jenks_bins': breaks.yb}, index=df_map[df_map[colName].notnull()].index)
    df_map = df_map.join(jenbin)
    df_map.jenks_bins.fillna(-1, inplace=True)

    # draw ward patches from polygons

    print 'Building Patches'

    df_map['patches'] = df_map['poly'].map(lambda x: PolygonPatch(
        x,
        fc='0.33',
        edgecolor='black', lw=.33,
        alpha=.9))

    print 'Last touches of color, with Jenks'

# Set colors using Jenks breaks
## Setup ColorMap
    colorm = plt.get_cmap('bwr')

    norm = colors.Normalize()
    pc = PatchCollection(df_map['patches'], match_original=True)

    pc.set_facecolor(colorm(norm(df_map['jenks_bins'].values)))

    print 'labels and scale'

    # Prepare the plt plot and axes
    plt.clf()
    fig = plt.figure()
    ax = fig.add_subplot(111, fc='w', frame_on=False)

    # Add a colour bar
    cb = colorbar_index(num_colors, colorm, shrink=0.5)
    cb.ax.tick_params(labelsize=6)

    print "get_bounds"

    newcoords = get_bounds(m,df_map)

    # DOES'T WORK, DOES NOT ACCEPT OSGB COORDS.
    # m.drawmapscale(
    #     newcoords[0], newcoords[1],
    #     coords[0], coords[1],
    #     10.,
    #     barstyle='fancy', labelstyle='simple',
    #     fillcolor1='w', fillcolor2='#555555',
    #     fontcolor='#555555',
    #     zorder=5)

    ax.add_collection(pc)

    print "axes and plotting!"

    ax.axis('auto')#; ax.axis('off')
    #set aspect ratio to latitude-longitude read
    ax.set_aspect( (newcoords[1]-newcoords[0]) / (newcoords[3]-newcoords[2]) )
    plt.show()

    return;

def get_bounds(m,df_map):
    # m = Basemap()
    # # Read in shapefile, without drawing anything
    # m.readshapefile("./Map/england_pcs_2012_wgs84", "patches", drawbounds=False)

    # initialize boundaries
    lon_min = 999999.
    lon_max = -999999.
    lat_min = 999999.
    lat_max = -999999.

    numindex = df_map['SHAPENUM'].tolist()
    numindex = map(int,numindex)

    for (shape, patch_name) in zip(m.map, m.map_info):
        if patch_name['SHAPENUM'] in numindex:
            lon, lat = zip(*shape)
            if min(lon) < lon_min:
                lon_min = min(lon)
            if max(lon) > lon_max:
                lon_max = max(lon)
            if min(lat) < lat_min:
                lat_min = min(lat)
            if max(lat) > lat_max:
                lat_max = max(lat)

    return lon_min, lat_min, lon_max, lat_max


def colorbar_index(ncolors, cmap, labels=None, **kwargs):
# Convenience functions for working with colour ramps and bars
# from Stephan Huegel - 2015 - http://sensitivecities.com/

    """
    This is a convenience function to stop you making off-by-one errors
    Takes a standard colour ramp, and discretizes it,
    then draws a colour bar with correctly aligned labels
    """
    cmap = cmap_discretize(cmap, ncolors)
    mappable = matplotlib.cm.ScalarMappable(cmap=cmap)
    mappable.set_array([])
    mappable.set_clim(-0.5, ncolors+0.5)
    colorbar = matplotlib.pyplot.colorbar(mappable, **kwargs)
    colorbar.set_ticks(np.linspace(0, ncolors, ncolors))
    colorbar.set_ticklabels(range(ncolors))
    if labels:
        colorbar.set_ticklabels(labels)
    return colorbar

def cmap_discretize(cmap, N):

    """
    Return a discrete colormap from the continuous colormap cmap.

        cmap: colormap instance, eg. cm.jet.
        N: number of colors.

    Example
        x = resize(arange(100), (5,100))
        djet = cmap_discretize(cm.jet, 5)
        imshow(x, cmap=djet)

    """
    if type(cmap) == str:
        cmap = matplotlib.pyplot.get_cmap(cmap)
    colors_i = np.concatenate((np.linspace(0, 1., N), (0., 0., 0., 0.)))
    colors_rgba = cmap(colors_i)
    indices = np.linspace(0, 1., N + 1)
    cdict = {}
    for ki, key in enumerate(('red', 'green', 'blue')):
        cdict[key] = [(indices[i], colors_rgba[i - 1, ki], colors_rgba[i, ki]) for i in xrange(N + 1)]
    return matplotlib.colors.LinearSegmentedColormap(cmap.name + "_%d" % N, cdict, 1024)
