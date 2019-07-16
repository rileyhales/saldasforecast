from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tethys_sdk.gizmos import SelectInput, RangeSlider

from .app import Saldasforecast as App
from .options import forecast_variables, wms_colors, geojson_colors, get_anomalytypes, get_charttypes, app_settings, \
    get_ensemblenumbers


@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    variables = SelectInput(
        display_text='Select SALDAS Variable',
        name='variables',
        multiple=False,
        original=True,
        options=forecast_variables(),
    )
    anominterval = SelectInput(
        display_text='Time Interval',
        name='anominterval',
        multiple=False,
        original=True,
        options=get_anomalytypes(),
    )
    ensemble = SelectInput(
        display_text='Filter Ensemble Number/Average',
        name='ensemble',
        multiple=False,
        original=True,
        options=get_ensemblenumbers(),
    )
    charttype = SelectInput(
        display_text='Choose a Plot Type',
        name='charttype',
        multiple=False,
        original=True,
        options=get_charttypes(),
    )

    colorscheme = SelectInput(
        display_text='SALDAS Data Color Scheme',
        name='colorscheme',
        multiple=False,
        original=True,
        options=wms_colors(),
        initial='rainbow'
    )

    opacity = RangeSlider(
        display_text='SALDAS Data Layer Opacity',
        name='opacity',
        min=.5,
        max=1,
        step=.05,
        initial=1,
    )

    gj_color = SelectInput(
        display_text='Boundary Border Colors',
        name='gjClr',
        multiple=False,
        original=True,
        options=geojson_colors(),
        initial='#ffffff'
    )

    gj_opacity = RangeSlider(
        display_text='Boundary Border Opacity',
        name='gjOp',
        min=0,
        max=1,
        step=.1,
        initial=1,
    )

    gj_weight = RangeSlider(
        display_text='Boundary Border Thickness',
        name='gjWt',
        min=1,
        max=5,
        step=1,
        initial=2,
    )

    gj_fillcolor = SelectInput(
        display_text='Boundary Fill Color',
        name='gjFlClr',
        multiple=False,
        original=True,
        options=geojson_colors(),
        initial='rgb(0,0,0,0)'
    )

    gj_fillopacity = RangeSlider(
        display_text='Boundary Fill Opacity',
        name='gjFlOp',
        min=0,
        max=1,
        step=.1,
        initial=.5,
    )

    context = {
        # data options
        'app': App.package,
        'variables': variables,
        'anominterval': anominterval,
        'ensemble': ensemble,
        'charttype': charttype,

        # display options
        'colorscheme': colorscheme,
        'opacity': opacity,
        'gjClr': gj_color,
        'gjOp': gj_opacity,
        'gjWt': gj_weight,
        'gjFlClr': gj_fillcolor,
        'gjFlOp': gj_fillopacity,

        # metadata
        'githublink': App.githublink,
        'datawebsite': App.datawebsite,
        'version': App.version,
        'settings': app_settings(),
    }

    return render(request, 'saldasforecast/home.html', context)
