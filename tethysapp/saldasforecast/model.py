def forecast_variables():
    """
    List of the plottable variables from the LIS Forecasts used in the app
    """
    return {
        'Air temperature': 'Tair_f_tavg',
        'Rainfall flux': 'Rainf_f_tavg',
        'Soil moisture content': 'SoilMoist_inst',
        'Total evapotranspiration': 'Evap_tavg',
    }


def get_wmscolors():
    """
    Color options usable by thredds wms
    """
    return [
        ('SST-36', 'sst_36'),
        ('Greyscale', 'greyscale'),
        ('Rainbow', 'rainbow'),
        ('OCCAM', 'occam'),
        ('OCCAM Pastel', 'occam_pastel-30'),
        ('Red-Blue', 'redblue'),
        ('NetCDF Viewer', 'ncview'),
        ('ALG', 'alg'),
        ('ALG 2', 'alg2'),
        ('Ferret', 'ferret'),
        ]


def app_configuration():
    """
    gets the settings for the app for use in other functions and ajax for leaflet
    """
    import os
    from .app import Saldasforecast
    return {
        'app_wksp_path': os.path.join(Saldasforecast.get_app_workspace().path, ''),
        'threddsurl': Saldasforecast.get_custom_setting("Thredds WMS URL"),
        'threddsdatadir': Saldasforecast.get_custom_setting("Local Thredds Folder Path"),
    }


def get_anomalytypes():
    return [
        ('Daily Anomaly', 'daily'),
        ('Dekad (10 day) Anomaly', 'dekad'),
        ('Monthly Anomaly', 'monthly')
    ]


def get_ensemblenumbers():
    return [
        ('Mean', '_mean.ncml'),
        (1, '_ens0.ncml'),
        (2, '_ens1.ncml'),
        (3, '_ens2.ncml'),
        (4, '_ens3.ncml'),
        (5, '_ens4.ncml'),
        (6, '_ens5.ncml'),
        (7, '_ens6.ncml'),
    ]


def get_charttypes():
    return [
        ('Single-Line Timeseries', 'singleline'),
        ('Multi-Line Timeseries', 'multiline'),
        ('Box-Whisker Plot', 'boxplot'),
    ]
