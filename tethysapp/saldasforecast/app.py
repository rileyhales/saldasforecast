from tethys_sdk.base import TethysAppBase, url_map_maker


class Saldasforecast(TethysAppBase):
    """
    Tethys app class for SALDAS Forecast Visualizer.
    """

    name = 'SALDAS Forecast Visualizer'
    index = 'saldasforecast:home'
    icon = 'saldasforecast/images/icon.gif'
    package = 'saldasforecast'
    root_url = 'saldasforecast'
    color = '#d35400'
    description = 'Shows animated maps of Forecasted LIS data for South Asia and creates analytical plots'
    tags = ''
    enable_feedback = False
    feedback_emails = []

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
        )

        return url_maps
