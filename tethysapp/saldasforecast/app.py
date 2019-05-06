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
    description = 'Shows animated maps of forecasted LIS data for south Asia and creates analytical plots'
    tags = ''
    enable_feedback = False
    feedback_emails = []
    updated = '6 May 2019'
    youtubelink = 'https://youtu.be/K123JFdRI5U'

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            # PRIMARY NAVIGABLE PAGES
            UrlMap(
                name='home',
                url='saldasforecast',
                controller='saldasforecast.controllers.home'
            ),

            # AJAX URLS
            UrlMap(
                name='customsettings',
                url='saldasforecast/ajax/customsettings',
                controller='saldasforecast.ajax.customsettings'
            ),
            UrlMap(
                name='customsettings',
                url='saldasforecast/ajax/timeseriesplot',
                controller='saldasforecast.ajax.timeseriesplot'
            ),
        )

        return url_maps

    def custom_settings(self):
        CustomSettings = (
            CustomSetting(
                name='Local Thredds Folder Path',
                type=CustomSetting.TYPE_STRING,
                description="Path to data in the folder mounted by Thredds (e.g. /Users/rileyhales/thredds/saldasforecast/)",
                required=True,
                # /Users/rileyhales/thredds/forecasts/
            ),
            CustomSetting(
                name='Thredds WMS URL',
                type=CustomSetting.TYPE_STRING,
                description="URL to the folder of GLDAS data and .ncml files on the thredds server (e.g. http://127.0.0.1:7000/thredds/wms/testAll/saldasforecast/)",
                required=True,
                # http://127.0.0.1:7000/thredds/wms/testAll/forecasts/
            ),
        )
        return CustomSettings
