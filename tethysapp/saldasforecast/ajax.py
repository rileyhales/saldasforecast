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
    plotdata['anominterval'] = str(data['anominterval']).capitalize()
    return JsonResponse(plotdata)


@login_required()
def get_spatialaverage(request):
    """
    Used to do averaging of a variable over a polygon of area, user drawn or a shapefile
    """
    from .tools import nc_to_gtiff, rastermask_average_gdalwarp
    from .model import forecast_variables
    import ast

    plotdata = {}
    data = ast.literal_eval(request.body.decode('utf-8'))
    data['times'], plotdata['units'] = nc_to_gtiff(data)
    plotdata['values'] = rastermask_average_gdalwarp(data)

    variables = forecast_variables()
    for key in variables:
        if variables[key] == data['variable']:
            name = key
            plotdata['name'] = name
            break
    plotdata['anominterval'] = str(data['anominterval']).capitalize()
    return JsonResponse(plotdata)


@login_required()
def customsettings(request):
    """
    returns the paths to the data/thredds services taken from the custom settings and gives it to the javascript
    """
    from .model import app_configuration
    return JsonResponse(app_configuration())
