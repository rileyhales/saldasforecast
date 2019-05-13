let districts_sld = '<?xml version="1.0" encoding="ISO-8859-1"?>\n' +
    '<StyledLayerDescriptor version="1.0.0" \n' +
    '    xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" \n' +
    '    xmlns="http://www.opengis.net/sld" \n' +
    '    xmlns:ogc="http://www.opengis.net/ogc" \n' +
    '    xmlns:xlink="http://www.w3.org/1999/xlink" \n' +
    '    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n' +
    '  <NamedLayer>\n' +
    '    <Name>Transparent polygon</Name>\n' +
    '    <UserStyle>\n' +
    '      <FeatureTypeStyle>\n' +
    '        <Rule>\n' +
    '          <PolygonSymbolizer>\n' +
    '            <Fill>\n' +
    '              <CssParameter name="fill">#0x000000</CssParameter>\n' +
    '            </Fill>\n' +
    '            <Stroke>\n' +
    '              <CssParameter name="stroke">#FFFFFF</CssParameter>\n' +
    '              <CssParameter name="stroke-width">2</CssParameter>\n' +
    '            </Stroke>\n' +
    '          </PolygonSymbolizer>\n' +
    '        </Rule>\n' +
    '      </FeatureTypeStyle>\n' +
    '    </UserStyle>\n' +
    '  </NamedLayer>\n' +
    '</StyledLayerDescriptor>';

////////////////////////////////////////////////////////////////////////  MAP FUNCTIONS
function map() {
    // create the map
    return L.map('map', {
        zoom: 4,
        minZoom: 2,
        boxZoom: true,
        maxBounds: L.latLngBounds(L.latLng(-100.0, -270.0), L.latLng(100.0, 270.0)),
        center: [27.25, 84],
        timeDimension: true,
        timeDimensionControl: true,
        timeDimensionControlOptions: {
            position: "bottomleft",
            autoPlay: true,
            loopButton: true,
            backwardButton: true,
            forwardButton: true,
            timeSliderDragUpdate: true,
            minSpeed: 1,
            maxSpeed: 6,
            speedStep: 1,
        },
    });
}

function basemaps() {
    // create the basemap layers
    let Esri_WorldImagery = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}');
    let Esri_WorldTerrain = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}', {maxZoom: 13});
    let Esri_Imagery_Labels = L.esri.basemapLayer('ImageryLabels');
    return {
        "ESRI Imagery": L.layerGroup([Esri_WorldImagery, Esri_Imagery_Labels]).addTo(mapObj),
        "ESRI Terrain": L.layerGroup([Esri_WorldTerrain, Esri_Imagery_Labels])
    }
}

function newLayer() {
    let wmsurl = wmsbase + $("#anominterval").val() + $("#ensemble").val();
    let wmsLayer = L.tileLayer.wms(wmsurl, {
        // version: '1.3.0',
        layers: $("#variables").val(),
        dimension: 'time',
        useCache: true,
        crossOrigin: false,
        format: 'image/png',
        transparent: true,
        opacity: $("#opacity").val(),
        BGCOLOR: '0x000000',
        styles: 'boxfill/' + $('#colors').val(),
        colorscalerange: '-15,15',
    });

    let timedLayer = L.timeDimension.layer.wms(wmsLayer, {
        name: 'time',
        requestTimefromCapabilities: true,
        updateTimeDimension: true,
        updateTimeDimensionMode: 'replace',
        cache: 20,
    }).addTo(mapObj);

    return timedLayer;
}

function districtboundaries() {
    return L.tileLayer.wms('https://tethys.byu.edu/geoserver/test/wms', {
        layers: 'test:NepalDistricts',
        format: 'image/png',
        transparent: true,
        opacity: 1,
        BGCOLOR: '0x000000',
        SLD_BODY: districts_sld,
    }).addTo(mapObj);
}

function makeControls() {
    return L.control.layers(basemapObj, {
        'GLDAS Layer': layerObj,
        'Point': drawnItems,
        'District Boundaries': districts
    }).addTo(mapObj);
}

function clearMap() {
    controlsObj.removeLayer(layerObj);
    controlsObj.removeLayer(districts);
    mapObj.removeLayer(layerObj);
    mapObj.removeLayer(districts);
    mapObj.removeControl(controlsObj);
}