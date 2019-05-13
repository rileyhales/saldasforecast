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
    updated = '13 May 2019'
    youtubelink = 'https://www.youtube.com/watch?v=r2o0oC8WaqQ'

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
                name='timeseriesplot',
                url='saldasforecast/ajax/timeseriesplot',
                controller='saldasforecast.ajax.timeseriesplot'
            ),
            UrlMap(
                name='getSpatialAverage',
                url='saldasforecast/ajax/getSpatialAverage',
                controller='saldasforecast.ajax.get_spatialaverage',
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
            ),
            CustomSetting(
                name='Thredds WMS URL',
                type=CustomSetting.TYPE_STRING,
                description="URL to the folder of GLDAS data and .ncml files on the thredds server (e.g. http://127.0.0.1:7000/thredds/wms/testAll/saldasforecast/)",
                required=True,
            ),
            CustomSetting(
                name='Geoserver Workspace URL',
                type=CustomSetting.TYPE_STRING,
                description="URL for this app's geoserver WMS enabled workspace (e.g. https://tethys.byu.edu/geoserver/test/wms)",
                required=True,
            ),
        )
        return CustomSettings
