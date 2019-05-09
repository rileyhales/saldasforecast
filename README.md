# SALDAS Forecast Visualizer Documentation
This is a Tethys 2/3 compatible app that visualizes forecasted LDAS data for the South Asia region. LDAS Forecasting by Ben Zaitchik and Yifan Zhou at John Hopkins University. App and analysis tools by Riley Hales and Jim Nelson at the Brigham Young University Hydroinformatics Lab. Research from 2018 through present.

## 1 Install the Tethys App
This application is compatible with Tethys 2.X and Tethys 3 Distributions and is compatible with both Python 2 and 3 and Django 1 and 2. Install the latest version of Tethys before installing this app. This app requires 2 python packages: numpy and netcdf4. Both should be installed automatically as part of this installation process.

On the terminal of the server enter the tethys environment with the ```t``` command. ```cd``` to the directory where you install apps then run the following commands:  
~~~~
git clone https://github.com/rileyhales/saldasforecast.git  
cd saldasforecast
python setup.py develop
~~~~  
If you are on a production server, run:
~~~~
tethys manage collectstatic
~~~~
Reset the server then attempt to log in through the web interface as an administrator. The app should appear in the Apps Library page in grey indicating you need to configure the custom settings.

## 2 Set up your Thredds Server
Refer to the documentation for Thredds to set up an instance of Thredds on your server.

In the public folder where your datasets are stored, create a new folder called ```saldasforecast```. Within that folder, create 3 additional folders named ```daily```, ```dekad```, and ```monthly``` which correspond to the time resolutions at which forecasted data are generated. Copy the most recent forecast data to the correspondingly named folders. If you are on the same server where the data are processed, set your workflow to output or move files to this location. 

Data in the is aggregated by year using NetCDF Markup Language (.ncml). The files you need are in the ncml folder of the app and you should copy them to the Thredds folder you just created. When you add new datasets each month, you will need to modify the ncml files to reflect the new starting month and year of the datasets you will be using.

If you did it correctly, your folder structure should exactly mirror this format:
~~~~
saldasforecast
--->daily
    --->(all the daily datasets go in this directory)
    --->ensemble member naming convention: daily.anomaly.YYYYMM.nc
    --->ensemble mean naming convention: daily.ensemble_mean_anomaly.nc
--->daily_ens0.ncml
--->daily_ens1.ncml
--->daily_ens2.ncml
    ...

--->dekad
    --->(all the dekad datasets go in this directory)
    --->ensemble member naming convention: dekad.anomaly.YYYYMM.nc
    --->ensemble mean naming convention: dekad.ensemble_mean_anomaly.nc
--->dekad_ens0.ncml
--->dekad_ens1.ncml
--->dekad_ens2.ncml
    ...

--->monthly
    --->(all the monthly datasets go in this directory)
    --->ensemble member naming convention: monthly.anomaly.YYYYMM.nc
    --->ensemble mean naming convention: monthly.ensemble_mean_anomaly.nc
--->monthly_ens0.ncml
--->monthly_ens1.ncml
--->monthly_ens2.ncml
    ...
~~~~
You will also need to modify Thredds' settings files to enable WMS services and support for netCDF files on your server. In the folder where you installed Thredds, there should be a file called ```catalog.xml```. 
~~~~
vim catalog.xml
~~~~
Type ```a``` to begin editing the document.

At the top of the document is a list of supported services. Make sure the line for wms is not commented out.
~~~~
<service name="wms" serviceType="WMS" base="/thredds/wms/" />
~~~~
Scroll down toward the end of the section that says ```filter```. This is the section that limits which kinds of datasets Thredds will process. We need it to accept .nc, .nc4, and .ncml file types. Make sure your ```filter``` tag includes the following lines.
~~~~
<filter>
    <include wildcard="*.nc"/>
    <include wildcard="*.nc4"/>
    <include wildcard="*.ncml"/>
</filter>
~~~~
Press ```esc``` then type ```:x!```  and press the ```return``` key to save and quit.
~~~~
vim threddsConfig.xml
~~~~
Find the section near the top about CORS (Cross-Origin Resource Sharing). CORS allows Thredds to serve data to servers besides the host where it is located. Depending on your exact setup, you need to enable CORS by uncommenting the tags.
~~~~
<CORS>
    <enabled>true</enabled>
    <maxAge>1728000</maxAge>
    <allowedMethods>GET</allowedMethods>
    <allowedHeaders>Authorization</allowedHeaders>
    <allowedOrigin>*</allowedOrigin>
</CORS>
~~~~
Press ```esc``` then type ```:x!```  and press the ```return``` key to save and quit.

You'll need to reset the Thredds server so the catalog is regenerated with the edits that you've made. The command to reset your server will vary based on your installation method such as ```docker reset thredds``` or ```sudo systemctl reset tomcat```.

## 3 Copy the newest forecasted LDAS data
The data shown on this app are currently hosted on the monsoon server of JHU. you want the split ensemble method of dividing datasets. Download those datasets and save them in the appropriately named folder you used previously (ie monthly, dekad, and monthly). Your new folder structure should look like this (ncml files excluded in this example):
~~~~
saldasforecast
--->daily
    --->daily.anomaly.201903.ens0.nc
        ...
    --->daily.ensemble_mean_anomaly.nc
    
--->dekad
    --->dekad.anomaly.201903.ens0.nc
        ...
    --->dekad.ensemble_mean_anomaly.nc
    
--->monthly
    --->monthly.anomaly.201903.ens0.nc
        ...
    --->monthly.ensemble_mean_anomaly.nc
~~~~

Verify that you have completed steps 2 and 3 correctly by viewing the Thredds catalog through a web browser. The default address will be something like ```yourserver.com/thredds/catalog.html```. Navigate to the ```Test all files...``` folder. Your ```saldasforecast``` folder should be visible. Open it and check that all your ```.ncml``` files are visible and that the ```.nc``` files are visible in the ```/3splitensemble``` directory. If they are not, review steps 2 and 3 and restart your Thredds server.

## 4 Set The Custom Settings
You need to specify 2 custom settings when you install the app. The file path to where you are storing the gldas netCDF files locally on the server and the base wms URL for the thredds server that will be serving the data.

**Local File Path:** This is the full path to the directory named saldasforecast that you should have created within the thredds data directory during step 2. You can get this by navigating to that folder in the terminal and then using the ```pwd``` command. (example: ```/tomcat/content/thredds/saldasforecast/```)  

**WMS base address:** This is the base that the app uses to build urls for each of the OGC WMS layers for the netcdf datasets. If you followed the typical configuration of thredds (these instructions) then your base url will look something like ```yourserver.com/thredds/wms/testAll/saldasforecast/```. You can verify this by opening the thredds catalog in a web browser (typically at ```yourserver.com/thredds/catalog.html```). Navigate to one of the LDAS netcdf files and click the WMS link. A page showing an xml document should load. Copy the url in the address bar until you get to the ```/saldasforecast/``` folder in that url. Do not include ```/3splitsensemble/name_of_dataset.nc``` or the request info that comes after it. (example: ```https://tethys.byu.edu/thredds/wms/testAll/saldasforecast/```)
