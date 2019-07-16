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
            minSpeed: 2,
            maxSpeed: 6,
            speedStep: 1,
        },
    });
}

function basemaps() {
    // create the basemap layers
    let Esri_WorldImagery = L.esri.basemapLayer('Imagery');
    let Esri_WorldTerrain = L.esri.basemapLayer('Terrain');
    let Esri_Imagery_Labels = L.esri.basemapLayer('ImageryLabels');
    return {
        "ESRI Imagery (labeled)": L.layerGroup([Esri_WorldImagery, Esri_Imagery_Labels]).addTo(mapObj),
        "ESRI Terrain (labeled)": L.layerGroup([Esri_WorldTerrain, Esri_Imagery_Labels]),
        "ESRI Imagery": Esri_WorldImagery,
        "ESRI Terrain": Esri_WorldTerrain
    }
}

////////////////////////////////////////////////////////////////////////  WMS LAYERS
function newLayer() {
    let layer = $("#variables").val();
    let wmsurl = threddsbase + $("#anominterval").val() + $("#ensemble").val();
    let cs_rng = bounds[layer];
    if ($("#use_csrange").is(":checked")) {
        cs_rng = String($("#cs_min").val()) + ',' + String($("#cs_max").val())
    }

    let wmsLayer = L.tileLayer.wms(wmsurl, {
        // version: '1.3.0',
        layers: layer,
        dimension: 'time',
        useCache: true,
        crossOrigin: false,
        format: 'image/png',
        transparent: true,
        opacity: $("#opacity_raster").val(),
        BGCOLOR: '0x000000',
        styles: 'boxfill/' + $('#colorscheme').val(),
        colorscalerange: cs_rng,
    });

    return L.timeDimension.layer.wms(wmsLayer, {
        name: 'time',
        requestTimefromCapabilities: true,
        updateTimeDimension: true,
        updateTimeDimensionMode: 'replace',
        cache: 20,
    }).addTo(mapObj);
}

////////////////////////////////////////////////////////////////////////  GEOJSON LAYERS
let currentregion = '';              // tracks which region is on the chart for updates not caused by the user picking a new region
function layerPopups(feature, layer) {
    let region = feature.properties.name;
    layer.bindPopup('<a class="btn btn-default" role="button" onclick="getShapeChart(' + "'" + region + "'" + ')">Get timeseries (average) for ' + region + '</a>');
}

// create all the geojson layers for world regions
const initstyle = {color: $("#gjClr").val(), opacity: $("#gjOp").val(), weight: $("#gjWt").val(), fillColor: $("#gjFlClr").val(), fillOpacity: $("#gjFlOp").val()};
let jsonparams = {onEachFeature: layerPopups, style: initstyle};

let districts = L.geoJSON(districts_json, jsonparams);
const geojsons = [districts];

function addGEOJSON() {
    for (let i in geojsons) {
        geojsons[i].addTo(mapObj)
    }
}

function styleGeoJSON() {
    // determine the styling to apply
    let style = {
        color: $("#gjClr").val(),
        opacity: $("#gjOp").val(),
        weight: $("#gjWt").val(),
        fillColor: $("#gjFlClr").val(),
        fillOpacity: $("#gjFlOp").val(),
    };
    // apply it to all the geojson layers
    for (let i in geojsons) {
        geojsons[i].setStyle(style);
    }
    usershape.setStyle(style);
}
////////////////////////////////////////////////////////////////////////  USERS CUSTOM UPLOADED SHAPEFILE
// gets the geojson layers from geoserver wfs and updates the layer
let usershape = L.geoJSON(false);
function getWFSData(gsworksp, shpname, gsurl) {
    let parameters = L.Util.extend({
        service: 'WFS',
        version: '1.0.0',
        request: 'GetFeature',
        typeName: gsworksp + ':' + shpname,
        maxFeatures: 10000,
        outputFormat: 'application/json',
        parseResponse: 'getJson',
        srsName: 'EPSG:4326',
        crossOrigin: 'anonymous'
    });
    $.ajax({
        async: true,
        jsonp: false,
        url: gsurl + L.Util.getParamString(parameters),
        contentType: 'application/json',
        success: function (data) {
            usershape.clearLayers();
            usershape.addData(data).addTo(mapObj);
            styleGeoJSON();
        },
    });
}

////////////////////////////////////////////////////////////////////////  LEGEND DEFINITIONS
let legend = L.control({position: 'topright'});
legend.onAdd = function () {
    let layer = $("#variables").val();
    let wmsurl = threddsbase + $("#anominterval").val() + $("#ensemble").val();
    let cs_rng = bounds[layer];
    if ($("#use_csrange").is(":checked")) {
        cs_rng = String($("#cs_min").val()) + ',' + String($("#cs_max").val())
    }

    let div = L.DomUtil.create('div', 'legend');
    let url = wmsurl + "?REQUEST=GetLegendGraphic&LAYER=" + layer + "&PALETTE=" + $('#colorscheme').val() + "&COLORSCALERANGE=" + cs_rng;
    div.innerHTML = '<img src="' + url + '" alt="legend" style="width:100%; float:right;">';
    return div
};

let latlon = L.control({position: 'bottomleft'});
latlon.onAdd = function () {
    let div = L.DomUtil.create('div', 'well well-sm');
    div.innerHTML = '<div id="mouse-position" style="text-align: center"></div>';
    return div;
};

////////////////////////////////////////////////////////////////////////  MAP CONTROLS AND CLEARING
// the layers box on the top right of the map
function makeControls() {
    return L.control.layers(basemapObj, {
        'Earth Observation': layerObj,
        'Drawing': drawnItems,
        'Uploaded Shapefile': usershape,
        'Districts': districts,
    }).addTo(mapObj);
}

// you need to remove layers when you make changes so duplicates dont persist and accumulate
function clearMap() {
    // remove the controls for the wms layer then remove it from the map
    controlsObj.removeLayer(layerObj);
    mapObj.removeLayer(layerObj);
    controlsObj.removeLayer(usershape);
    mapObj.removeLayer(usershape);
    // now do it for all the geojson layers
    for (let i in geojsons) {
        controlsObj.removeLayer(geojsons[i]);
        mapObj.removeLayer(geojsons[i]);
    }
    // now delete the controls object
    mapObj.removeControl(controlsObj);
}
