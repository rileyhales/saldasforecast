from .app import Saldasforecast as App
import os


def app_settings():
    """
    Gets the settings for the app for use in other functions and ajax for leaflet
    Dependencies: os, App (app)
    """
    return {
        'app_wksp_path': os.path.join(App.get_app_workspace().path, ''),
        'threddsdatadir': App.get_custom_setting("Local Thredds Folder Path"),
        'threddsurl': App.get_custom_setting("Thredds WMS URL"),
    }


def forecast_variables():
    """
    List of the plottable variables from the GLDAS 2.1 datasets used
    """
    return [
        ('Air temperature', 'Tair_f_tavg'),
        ('Rainfall flux', 'Rainf_f_tavg'),
        ('Soil moisture content', 'SoilMoist_inst'),
        ('Total evapotranspiration', 'Evap_tavg'),
    ]


def get_anomalytypes():
    return [
        ('Monthly Anomaly', 'monthly'),
        ('Dekad (10 day) Anomaly', 'dekad'),
        # ('Daily Anomaly', 'daily'),
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


def wms_colors():
    """
    Color options usable by thredds wms
    """
    return [
        ('SST-36', 'sst_36'),
        ('Precipitaiton', 'precipitation'),
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


def geojson_colors():
    return [
        ('White', '#ffffff'),
        ('Transparent', 'rgb(0,0,0,0)'),
        ('Red', '#ff0000'),
        ('Green', '#00ff00'),
        ('Blue', '#0000ff'),
        ('Black', '#000000'),
        ('Pink', '#ff69b4'),
        ('Orange', '#ffa500'),
        ('Teal', '#008080'),
        ('Purple', '#800080'),
    ]


def get_charttypes():
    return [
        ('Single-Line Timeseries', 'singleline'),
        ('Ensemble Stats (Multi-Line Plot)', 'multiline'),
        ('Ensemble Stats (Box Plot)', 'boxplot'),
    ]
