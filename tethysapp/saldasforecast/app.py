from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import CustomSetting


class Saldasforecast(TethysAppBase):
    """
    Tethys app class for SALDAS Forecast Visualizer.
    """

    name = 'SALDAS Forecast Visualizer'
    index = 'saldasforecast:home'
    icon = 'saldasforecast/images/weathericon.png'
    package = 'saldasforecast'
    root_url = 'saldasforecast'
    color = '#d35400'
    description = 'Shows animated maps of Forecasted LIS data for South Asia and creates analytical plots'
    tags = ''
    enable_feedback = False
    feedback_emails = []
    updated = '23 April 2019'

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='saldasforecast',
                controller='saldasforecast.controllers.home'
            ),
            UrlMap(
                name='customsettings',
                url='saldasforecast/ajax/customsettings',
                controller='saldasforecast.ajax.customsettings'
            ),
        )

        return url_maps

    def custom_settings(self):
        CustomSettings = (
            CustomSetting(
                name='Local Thredds Folder Path',
                type=CustomSetting.TYPE_STRING,
                description="Path to data in the folder mounted by Thredds (e.g. /home/thredds/myDataFolder/)",
                required=True,
                # /Users/rileyhales/thredds/forecasts/
            ),
            CustomSetting(
                name='Thredds WMS URL',
                type=CustomSetting.TYPE_STRING,
                description="URL to the folder of GLDAS data and .ncml files on the thredds server (e.g. tethys.byu.edu/thredds/myDataFolder/)",
                required=True,
                # http://127.0.0.1:7000/thredds/wms/testAll/forecasts/
            ),
        )
        return CustomSettings
