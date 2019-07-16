from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import CustomSetting


class Saldasforecast(TethysAppBase):
    """
    Tethys app class for SALDAS Drought Forecast Tool.
    """

    name = 'SALDAS Drought Forecast Tool'
    index = 'saldasforecast:home'
    icon = 'saldasforecast/images/weathericon.png'
    package = 'saldasforecast'
    root_url = 'saldasforecast'
    color = '#d35400'
    description = 'Place a brief description of your app here.'
    tags = ''
    enable_feedback = False
    feedback_emails = []
    githublink = 'https://github.com/rileyhales/saldasforecast'
    datawebsite = ''
    version = 'dev 7/2019'

    def url_maps(self):
        """
        Add controllers
        """
        urlmap = url_map_maker(self.root_url)

        url_maps = (
            # url maps to navigable pages
            urlmap(
                name='home',
                url='saldasforecast',
                controller='saldasforecast.controllers.home'
            ),

            # url maps for ajax calls
            urlmap(
                name='getChart',
                url='saldasforecast/ajax/getChart',
                controller='saldasforecast.ajax.getchart',
            ),
            urlmap(
                name='uploadShapefile',
                url='saldasforecast/ajax/uploadShapefile',
                controller='saldasforecast.ajax.uploadshapefile',
            ),

        )
        return url_maps

    def custom_settings(self):
        custom_settings = (
            CustomSetting(
                name='Local Thredds Folder Path',
                type=CustomSetting.TYPE_STRING,
                description="Local file path to datasets (same as used by Thredds) (e.g. /home/thredds/myDataFolder/)",
                required=True,
            ),
            CustomSetting(
                name='Thredds WMS URL',
                type=CustomSetting.TYPE_STRING,
                description="URL to the GLDAS folder on the thredds server (e.g. http://[host]/thredds/saldasforecast/)",
                required=True,
            ),
            CustomSetting(
                name='GeoserverURL',
                type=CustomSetting.TYPE_STRING,
                description="Include http or https but no '/' after /geoserver, ex: https://tethys.byu.edu/geoserver",
                required=False,
            ),
            CustomSetting(
                name='Geoserver user/pass',
                type=CustomSetting.TYPE_STRING,
                description="Admin credentials for uploading shapefiles to geoserver in the format username/password",
                required=False,
            ),
        )
        return custom_settings
