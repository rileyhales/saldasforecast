import calendar
import datetime
import os
import shutil

import gdal
import gdalnumeric
import netCDF4
import numpy
import osr
import ogr
import json
import statistics

from .app import Saldasforecast as App
from .model import app_configuration

def ts_plot(data):
    """
    Description: generates a timeseries for a given point and given variable defined by the user.
    Arguments: A dictionary object from the AJAX-ed JSON object that contains coordinates and the variable name.
    Author: Riley Hales
    Dependencies: netcdf4, numpy, datetime
    Last Updated: Oct 11 2018
    """
    plotdata = {}
    values = []
    variable = str(data['variable'])
    coords = data['coords']
    anominterval = data['anominterval']

    # get a list of all the netcdf files but only include the ensemble members, not monthly means
    configs = app_configuration()
    path = os.path.join(configs['threddsdatadir'], anominterval)
    allfiles = os.listdir(path)
    files = [nc for nc in allfiles if nc.startswith(anominterval + '.anomaly')]
    files.sort()
    del configs

    # find the point of data array that corresponds to the user's choice, get the units of that variable
    datapath = os.path.join(path, str(files[0]))
    dataset = netCDF4.Dataset(datapath, 'r')
    nc_lons = dataset['lon'][:]
    nc_lats = dataset['lat'][:]
    adj_lon_ind = (numpy.abs(nc_lons - coords[0])).argmin()
    adj_lat_ind = (numpy.abs(nc_lats - coords[1])).argmin()
    plotdata['units'] = dataset[variable].__dict__['units']
    dataset.close()
    uniquedates = []

    # extract values at each timestep
    for nc in files:
        # set the time value for each file
        datapath = os.path.join(path, nc)
        dataset = netCDF4.Dataset(datapath, 'r')
        # get rid of the starter characters, slice the string to get the timestep
        time = nc.replace(anominterval, '')
        time = time.replace('.anomaly.', '').replace('.ens_mean_anomaly.', '')[0:6]
        t_step = datetime.datetime.strptime(time, "%Y%m")
        t_step = calendar.timegm(t_step.utctimetuple()) * 1000
        if t_step not in uniquedates:
            uniquedates.append(t_step)
        for ensemble, var in enumerate(dataset[variable][:]):
            # get the value at the point
            val = float(dataset[variable][0, adj_lat_ind, adj_lon_ind].data)
            values.append((t_step, val))
        dataset.close()
    uniquedates.sort()
    plotdata['singleline'] = values

    # process the timeseries values into the multiline and box plots formats
    plotdata['multiline'] = {'min': [], 'max': [], 'mean': []}
    plotdata['boxplot'] = []
    for date in uniquedates:
        # create a list of values for each day
        dailyvalues = []
        for value in values:
            if value[0] == date:
                dailyvalues.append(value[1])
        dailyvalues.sort()
        # process the daily values for the multiline plot
        daymin = min(dailyvalues)
        daymax = max(dailyvalues)
        mean = sum(dailyvalues)/len(dailyvalues)
        plotdata['multiline']['min'].append((date, daymin))
        plotdata['multiline']['max'].append((date, daymax))
        plotdata['multiline']['mean'].append((date, mean))
        # get statistics for the box plot format, if its not the average
        std = statistics.stdev(dailyvalues)
        plotdata['boxplot'].append([date, daymin, mean - std, mean, mean + std, daymax])

    return plotdata


def nc_to_gtiff(data):
    """
    Description: This script accepts a netcdf file in a geographic coordinate system, specifically the NASA GLDAS
        netcdfs, and extracts the data from one variable and the lat/lon steps to create a geotiff of that information.
    Dependencies:
        netCDF4, numpy, gdal, osr, os, shutil, calendar, datetime
        from .app import Gldas as App
        from .model import app_configuration
    Params: View README.md
    Returns: Creates a geotiff named 'geotiff.tif' in the directory specified
    Author: Riley Hales, RCH Engineering, March 2019
    """
    var = str(data['variable'])
    anominterval = data['anominterval']
    configs = app_configuration()
    data_dir = configs['threddsdatadir']
    times = []
    units = ''

    path = os.path.join(data_dir, anominterval)
    allfiles = os.listdir(path)
    files = [nc for nc in allfiles if nc.startswith(anominterval + '.ens')]
    files.sort()

    # Remove old geotiffs before filling it
    geotiffdir = os.path.join(App.get_app_workspace().path, 'geotiffs')
    if os.path.isdir(geotiffdir):
        shutil.rmtree(geotiffdir)
    os.mkdir(geotiffdir)

    for i in range(len(files)):
        # open the netcdf and copy data from it
        nc_obj = netCDF4.Dataset(os.path.join(path, str(files[i])), 'r')
        var_data = nc_obj.variables[var][:]
        lat = nc_obj.variables['lat'][:]
        lon = nc_obj.variables['lon'][:]
        units = nc_obj[var].__dict__['units']

        # create the timesteps for the highcharts plot
        t_value = (nc_obj['time'].__dict__['units'])
        t_step = datetime.datetime.strptime(t_value, "days since %Y-%m-%d 00:00:00")
        times.append(calendar.timegm(t_step.utctimetuple()) * 1000)

        # format the array of information going to the tiff
        array = numpy.asarray(var_data)[0, :, :]
        array[array < -9000] = numpy.nan                # change the comparator to git rid of the fill value
        array = array[::-1]       # vertically flip the array so the orientation is right (you just have to, try it)

        # Creates geotiff raster file (filepath, x-dimensions, y-dimensions, number of bands, datatype)
        gtiffpath = os.path.join(geotiffdir, 'geotiff' + str(i) + '.tif')
        gtiffdriver = gdal.GetDriverByName('GTiff')
        new_gtiff = gtiffdriver.Create(gtiffpath, len(lon), len(lat), 1, gdal.GDT_Float32)

        # geotransform (sets coordinates) = (x-origin(left), x-width, x-rotation, y-origin(top), y-rotation, y-width)
        yorigin = lat.max()
        xorigin = lon.min()
        xres = lat[1] - lat[0]
        yres = lon[1] - lon[0]
        new_gtiff.SetGeoTransform((xorigin, xres, 0, yorigin, 0, -yres))

        # Set projection of the geotiff (Projection EPSG:4326, Geographic Coordinate System WGS 1984 (degrees lat/lon)
        new_gtiff.SetProjection(osr.SRS_WKT_WGS84)

        # actually write the data array to the tiff file and save it
        new_gtiff.GetRasterBand(1).WriteArray(array)      # write band to the raster (variable array)
        new_gtiff.FlushCache()                            # write to disk
    return times, units


def rastermask_average_gdalwarp(data):
    """
    Description: A function to mask/clip a raster by the boundaries of a shapefile and computer the average value of the
        resulting raster
    Dependencies:
        gdal, gdalnumeric, numpy, os, shutil, ogr, json
        from .app import Gldas as App
    Params: View README.md
    Returns: mean value of an array within a shapefile's boundaries
    Author: Riley Hales, RCH Engineering, April 2019
    """

    values = []
    times = data['times']
    times.sort()
    shppath = ''
    wrkpath = App.get_app_workspace().path

    if data['shapefile'] == 'true':
        shppath = os.path.join(wrkpath, 'NepalDistricts', 'NepalDistricts.shp')
    else:
        # todo: still under development- turn a geojson into a shapefile
        print('ya can\'t do that yet')

    # setup the working directories for the geoprocessing
    geotiffdir = os.path.join(wrkpath, 'geotiffs')
    geotiffs = os.listdir(geotiffdir)

    # perform the gropreccesing on each file in the geotiff directory
    for i in range(len(geotiffs)):
        # clip the raster
        inraster = gdal.Open(os.path.join(geotiffdir, 'geotiff' + str(i) + '.tif'))
        savepath = os.path.join(geotiffdir, 'outraster.tif')
        clippedraster = gdal.Warp(savepath, inraster, format='GTiff', cutlineDSName=shppath, dstNodata=numpy.nan,) # cutlineSQL="SELECT * FROM COLUMNS WHERE DCODE='" + str(data['distnum']) + "'",)
        # do the averaging math on the raster as an array
        array = gdalnumeric.DatasetReadAsArray(clippedraster)
        array = array.flatten()
        array = array[~numpy.isnan(array)]
        mean = array.mean()
        values.append((times[i], float(mean)))

    if os.path.isdir(geotiffdir):
        shutil.rmtree(geotiffdir)

    return values
