from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required()
def generatePlot(request):
    """
    The controller for the ajax call to create a timeseries for the area chosen by the user's drawing
    """
    from .model import forecast_variables
    from .tools import ts_plot
    import ast

    data = ast.literal_eval(request.body.decode('utf-8'))
    response_object = {}
    plot_items = ts_plot(data)
    response_object['units'] = plot_items[0]
    response_object['values'] = plot_items[1]
    variables = forecast_variables()
    for key in variables:
        if variables[key] == data['variable']:
            name = key
            break
    response_object['name'] = name
    return JsonResponse(response_object)


@login_required()
def customsettings(request):
    """
    returns the paths to the data/thredds services taken from the custom settings and gives it to the javascript
    """
    from .model import app_configuration
    return JsonResponse(app_configuration())
