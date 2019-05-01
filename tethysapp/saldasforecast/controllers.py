from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import SelectInput, RangeSlider
from .app import Saldasforecast as App
from .model import forecast_variables, get_wmscolors, get_times, get_anomalytypes, get_ensemblenumbers


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
        initial='Soil moisture content',
    )

    colors = SelectInput(
        display_text='Color Scheme',
        name='colors',
        multiple=False,
        options=get_wmscolors(),
        initial='Rainbow',
    )

    # dates = SelectInput(
    #     display_text='Time Interval',
    #     name='dates',
    #     multiple=False,
    #     options=get_times(),
    # )

    anomaly = SelectInput(
        display_text='Select Anomaly Data',
        name='anomaly',
        multiple=False,
        options=get_anomalytypes(),
    )

    ensemble = SelectInput(
        display_text='Select Ensemble Number',
        name='ensemble',
        multiple=False,
        options=get_ensemblenumbers(),
        initial='ens0.ncml',
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
        # 'dates': dates,
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
