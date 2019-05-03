from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required()
def timeseriesplot(request):
    """
    The controller for the ajax call to create a timeseries for the area chosen by the user's drawing
    """
    from .model import forecast_variables
    from .tools import ts_plot
    import ast
    data = ast.literal_eval(request.body.decode('utf-8'))
    plotdata = ts_plot(data)
    variables = forecast_variables()
    for key in variables:
        if variables[key] == data['variable']:
            name = key
            break
    plotdata['name'] = name
    return JsonResponse(plotdata)


@login_required()
def customsettings(request):
    """
    returns the paths to the data/thredds services taken from the custom settings and gives it to the javascript
    """
    from .model import app_configuration
    return JsonResponse(app_configuration())
