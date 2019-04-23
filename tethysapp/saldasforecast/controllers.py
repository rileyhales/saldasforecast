from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import SelectInput, RangeSlider
from .app import Saldasforecast as App
from .model import forecast_variables, wms_colors, get_times


@login_required()
def home(request):
    """
    Controller for the app home page.
    """

    variables = forecast_variables()
    options = []
    for key in sorted(variables.keys()):
        tuple1 = (key, variables[key])
        options.append(tuple1)
    del tuple1, key, variables

    variables = SelectInput(
        display_text='Select GLDAS Variable',
        name='variables',
        multiple=False,
        original=True,
        options=options,
    )

    colors = SelectInput(
        display_text='Color Scheme',
        name='colors',
        multiple=False,
        options=wms_colors(),
    )

    dates = SelectInput(
        display_text='Time Interval',
        name='dates',
        multiple=False,
        options=get_times(),
    )

    ensemble = RangeSlider(
        display_text='Ensemble Number',
        name='ensemble',
        min=1,
        max=7,
        step=1,
        initial=1,
    )

    opacity = RangeSlider(
        display_text='Layer Opacity',
        name='opacity',
        min=.4,
        max=1,
        step=.05,
        initial=.8,
    )

    context = {
        'variables': variables,
        'opacity': opacity,
        'colors': colors,
        'ensemble': ensemble,
        'dates': dates,
        'updated': App.updated,
    }

    return render(request, 'saldasforecast/home.html', context)