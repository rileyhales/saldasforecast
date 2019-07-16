import ast
import os
import zipfile
import subprocess
import shutil

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .charts import newchart
from .app import Saldasforecast as App


@login_required()
def getchart(request):
    """
    Used to make a timeseries of a variable at a user drawn point
    Dependencies: gldas_variables (options), pointchart (tools), ast, makestatplots (tools)
    """
    data = ast.literal_eval(request.body.decode('utf-8'))
    data['user'] = request.user
    data = newchart(data)
    return JsonResponse(data)


@login_required()
def uploadshapefile(request):
    files = request.FILES.getlist('files')
    user = request.user
    user_workspace = App.get_user_workspace(user).path

    # delete old files in the directory
    if os.path.exists(user_workspace):
        shutil.rmtree(user_workspace)
        os.mkdir(user_workspace)

    # write the new files to the directory
    for n, file in enumerate(files):
        with open(os.path.join(user_workspace, file.name), 'wb') as dst:
            for chunk in files[n].chunks():
                dst.write(chunk)

    # check that the user has provided geoserver settings
    cs = App.get_custom_setting('Geoserver user/pass')
    gsurl = App.get_custom_setting('GeoserverURL')
    if cs is None or gsurl is None:
        return JsonResponse({'status': 'uploaded'})

    # rename the files and create a zip archive
    files = os.listdir(user_workspace)
    zippath = os.path.join(user_workspace, str(user) + '.zip')
    archive = zipfile.ZipFile(zippath, mode='w')
    for file in files:
        archive.write(os.path.join(user_workspace, file), arcname=file)
    archive.close()

    # upload the archive to geoserver
    shellpath = os.path.join(App.get_app_workspace().path, 'upload_shapefile.sh')
    v1 = cs.split('/')[0]
    v2 = cs.split('/')[1]
    v3 = zippath
    v4 = gsurl
    v5 = App.package
    v6 = files[0].split('.')[0]
    subprocess.call(['bash', shellpath, v1, v2, v3, v4, v5, v6])

    return JsonResponse({'gsurl': v4 + '/' + v5 + '/ows', 'gsworksp': v5, 'shpname': v6})
