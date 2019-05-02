from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import SelectInput, RangeSlider
from .app import Saldasforecast as App
from .model import forecast_variables, get_wmscolors, get_anomalytypes, get_ensemblenumbers


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
        display_text='Select LDAS Variable',
        name='variables',
        multiple=False,
        original=True,
        options=options,
        initial='Air temperature',
    )

    colors = SelectInput(
        display_text='Color Scheme',
        name='colors',
        multiple=False,
        original=True,
        options=get_wmscolors(),
        initial='Rainbow',
    )

    anomaly = SelectInput(
        display_text='Choose Anomaly Type',
        name='anomaly',
        multiple=False,
        original=True,
        options=get_anomalytypes(),
    )

    ensemble = SelectInput(
        display_text='Pick Ensemble Number',
        name='ensemble',
        multiple=False,
        original=True,
        options=get_ensemblenumbers(),
    )

    opacity = RangeSlider(
        display_text='Layer Opacity',
        name='opacity',
        min=.4,
        max=1,
        step=.025,
        initial=.8,
    )

    context = {
        'variables': variables,
        'opacity': opacity,
        'colors': colors,
        'ensemble': ensemble,
        'anomaly': anomaly,
        'updated': App.updated,
    }

    return render(request, 'saldasforecast/home.html', context)


@login_required()
def otherpage(request):
    """
    Controller for the app home page.
    """
    context = {
        'updated': App.updated,
    }
    return render(request, 'saldasforecast/otherpage.html', context)
