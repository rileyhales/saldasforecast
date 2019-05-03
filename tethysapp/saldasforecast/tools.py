def ts_plot(data):
    """
    Description: generates a timeseries for a given point and given variable defined by the user.
    Arguments: A dictionary object from the AJAX-ed JSON object that contains coordinates and the variable name.
    Author: Riley Hales
    Dependencies: netcdf4, numpy, datetime
    Last Updated: Oct 11 2018
    """
    from .model import app_configuration
    import netCDF4, numpy, datetime, os, calendar, statistics

    plotdata = {}
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
    plotdata['units'] = dataset[variable].__dict__['units']
    dataset.close()
    uniquedates = []

    # extract values at each timestep
    for nc in files:
        # set the time value for each file
        datapath = os.path.join(path, nc)
        dataset = netCDF4.Dataset(datapath, 'r')
        time = nc.replace(anomtype, '').replace('.', '')[0:6]
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
        daymin = min(dailyvalues)
        daymax = max(dailyvalues)
        mean = sum(dailyvalues)/len(dailyvalues)
        std = statistics.stdev(dailyvalues)
        # sort the daily values for the multiline plot
        plotdata['multiline']['min'].append((date, daymin))
        plotdata['multiline']['max'].append((date, daymax))
        plotdata['multiline']['mean'].append((date, mean))
        # get statistics for the box plot format
        plotdata['boxplot'].append([daymin, mean - std, mean, mean + std, daymax])

    return plotdata
