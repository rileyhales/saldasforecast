def forecast_variables():
    """
    List of the plottable variables from the LIS Forecasts used in the app
    """
    return {
        '2-m air temperature over vegetated part': 'VegT2m_tavg',
        '2-m specific humidity over vegetation': 'QairT2m_tavg',
        'Absorbed photosynthesis active radiation energy by canopy': 'APAR_tavg',
        'Actual number of snow layers': 'ActSnowNL_tavg',
        'Air temperature': 'Tair_f_tavg_max',
        'Average ground surface temperature': 'AvgGrndT_tavg',
        'Average layer fraction of liquid moisture': 'SmLiqFrac_inst',
        'Bare soil evaporation': 'ESoil_tavg',
        'Bare soil temperature': 'BareSoilT_tavg',
        'Canopy air temperature': 'VegCanopT_tavg',
        'Canopy air vapor pressure': 'CanopVP_tavg',
        'Canopy temperature': 'VegT_tavg',
        'Canopy wet fraction': 'CanopWetFrac_tavg',
        'Eastward wind': 'EWind_f_tavg',
        'Emissivity': 'Emiss_f_tavg',
        'Ensemble numbers': 'ensemble',
        'Green vegetation fraction': 'Greenness_inst',
        'Gross primary production': 'GPP_tavg',
        'Intercepted liquid water': 'CanopIntLiq_tavg',
        'Interception evaporation': 'ECanop_tavg',
        'Latent heat flux': 'Qle_tavg',
        # 'Latitude': 'lat',
        'Leaf area index': 'LAI_inst',
        # 'Longitude': 'lon',
        'Net downward longwave radiation': 'Lwnet_tavg',
        'Net downward shortwave radiation': 'Swnet_tavg',
        'Net ecosystem exchange': 'NEE_tavg',
        'Net primary productivity': 'NPP_tavg',
        'Northward wind': 'NWind_f_tavg',
        'Rainfall flux': 'Rainf_f_tavg',
        'Sensible heat flux': 'Qh_tavg',
        'Snow age': 'SnowAge_tavg',
        'Snow cover': 'Snowcover_inst',
        'Snow depth': 'SnowDepth_inst',
        'Snow ice': 'SnowIce_tavg',
        'Snow water equivalent': 'SWE_inst',
        'Snow-layer liquid water': 'SnowLiq_tavg',
        'Snowmelt': 'Qsm_tavg',
        'Soil heat flux': 'Qg_tavg',
        'Soil moisture content': 'SoilMoist_inst',
        'Soil temperature': 'SoilTemp_inst',
        'Solar radiation absorbed by ground': 'SAG_tavg',
        'Solar radiation absorbed by vegetation': 'SAV_tavg',
        'Specific humidity': 'Qair_f_tavg',
        'Stem area index': 'SAI_inst',
        'Subsurface runoff amount': 'Qsb_tavg',
        'Surface albedo': 'Albedo_inst',
        'Surface downward longwave radiation': 'LWdown_f_tavg',
        'Surface downward shortwave radiation': 'SWdown_f_tavg',
        'Surface pressure': 'Psurf_f_tavg',
        'Surface radiative temperature': 'RadT_tavg',
        'Surface runoff': 'Qs_tavg',
        'Surface temperature': 'AvgSurfT_tavg',
        'Terrestrial water storage': 'TWS_inst',
        # 'Time': 'time',
        'Total evapotranspiration': 'Evap_tavg',
        'Total precipitation amount': 'TotalPrecip_tavg',
        'Total reflected solar radiation': 'SwReflect_tavg',
        'Vegetation transpiration': 'TVeg_tavg',
        'Water table depth': 'WaterTableD_inst',
        'Wind speed': 'Wind_f_tavg'
    }


def wms_colors():
    """
    Color options usable by thredds wms
    """
    return [
        ('SST-36', 'sst_36'),
        ('Greyscale', 'greyscale'),
        ('Rainbox', 'rainbow'),
        ('OCCAM', 'occam'),
        ('OCCAM Pastel', 'occam_pastel-30'),
        ('Red-Blue', 'redblue'),
        ('NetCDF Viewer', 'ncview'),
        ('ALG', 'alg'),
        ('ALG 2', 'alg2'),
        ('Ferret', 'ferret'),
        # ('Probability', 'prob'),
        # ('White-Blue', whiteblue'),
        # ('Grace', 'grace'),
        ]


def get_times():
    """
    Time intervals of GLDAS data
    """
    return [
        (2019, 2019),
        (2018, 2018),
        (2017, 2017),
        (2016, 2016),
        (2015, 2015),
        (2014, 2014),
        (2013, 2013),
        (2012, 2012),
        (2011, 2011),
        (2010, 2010),
        (2009, 2009),
        (2008, 2008),
        (2007, 2007),
        (2006, 2006),
        (2005, 2005),
        (2004, 2004),
        (2003, 2003),
        (2002, 2002),
        (2001, 2001),
        (2000, 2000),
        ('All Available Times', 'alltimes'),
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
