def ts_plot(data):
    """
    Description: generates a timeseries for a given point and given variable defined by the user.
    Arguments: A dictionary object from the AJAX-ed JSON object that contains coordinates and the variable name.
    Author: Riley Hales
    Dependencies: netcdf4, numpy, datetime, random
    Last Updated: Oct 11 2018
    """
    from .model import app_configuration
    import netCDF4, numpy, datetime, os, calendar

    values = []
    variable = str(data['variable'])
    coords = data['coords']
    anomtype = data['anomaly']

    configs = app_configuration()
    path = os.path.join(configs['threddsdatadir'], '3splitensemble')
    allfiles = os.listdir(path)
    files = [nc for nc in allfiles if nc.startswith(anomtype)]
    files.sort()
    del configs

    # find the point of data array that corresponds to the user's choice, get the units of that variable
    datapath = os.path.join(path, str(files[0]))
    dataset = netCDF4.Dataset(datapath, 'r')
    nc_lons = dataset['lon'][:]
    nc_lats = dataset['lat'][:]
    adj_lon_ind = (numpy.abs(nc_lons - coords[0])).argmin()
    adj_lat_ind = (numpy.abs(nc_lats - coords[1])).argmin()
    units = dataset[variable].__dict__['units']
    dataset.close()

    # extract values at each timestep
    for nc in files:
        # set the time value for each file
        datapath = os.path.join(path, nc)
        dataset = netCDF4.Dataset(datapath, 'r')
        # t_value = (dataset['time'].__dict__['begin_date'])
        time = nc.replace('stdanomaly.', '').replace('anomaly.', '')[0:6]
        t_step = datetime.datetime.strptime(time, "%Y%m")
        t_step = calendar.timegm(t_step.utctimetuple()) * 1000
        for ensemble, var in enumerate(dataset[variable][:]):
            # get the value at the point
            val = float(dataset[variable][0, adj_lat_ind, adj_lon_ind].data)
            values.append((t_step, val))
        dataset.close()

    return_items = [units, values]

    return return_items
