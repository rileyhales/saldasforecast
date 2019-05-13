// Getting the csrf token
let csrftoken = Cookies.get('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

////////////////////////////////////////////////////////////////////////  LOAD THE MAP
function getThreddswms() {              // get the url paths to start drawing maps
    $.ajax({
        url: '/apps/saldasforecast/ajax/customsettings/',
        async: false,
        data: '',
        dataType: 'json',
        contentType: "application/json",
        method: 'POST',
        success: function (result) {
            threddsbase = result['threddsurl'];
            geoserverbase = result['geoserverurl'];
        },
    });
}

let threddsbase;
let geoserverbase;
getThreddswms();                        // sets the value of wmsbase
const mapObj = map();                   // used by legend and draw controls
const basemapObj = basemaps();          // used in the make controls function
let districts = districtboundaries();   // the district boundaries layer
legend.addTo(mapObj);                   // the color scale/legend

////////////////////////////////////////////////////////////////////////  SETUP DRAWING AND LAYER CONTROLS
let drawnItems = new L.FeatureGroup().addTo(mapObj);      // FeatureGroup is to store editable layers
let drawControl = new L.Control.Draw({
    edit: {
        featureGroup: drawnItems,
        edit: false,
    },
    draw: {
        polyline: false,
        circlemarker: false,
        circle: false,
        polygon: false,
        rectangle: false,
    },
});
mapObj.addControl(drawControl);
mapObj.on("draw:drawstart ", function () {     // control what happens when the user draws things on the map
    drawnItems.clearLayers();
});
mapObj.on(L.Draw.Event.CREATED, function (event) {
    drawnItems.addLayer(event.layer);
    L.Draw.Event.STOP;
    getChart(drawnItems);
    // e.layer.addTo(drawnItems);
});

let layerObj = newLayer();              // adds the wms raster layer
let controlsObj = makeControls();       // the layer toggle controls top-right corner

////////////////////////////////////////////////////////////////////////  EVENT LISTENERS
$("#anominterval").change(function () {
    clearMap();
    layerObj = newLayer();
    controlsObj = makeControls();
    getChart(drawnItems);
    legend.addTo(mapObj);
});

$("#ensemble").change(function () {
    clearMap();
    layerObj = newLayer();
    controlsObj = makeControls();
    legend.addTo(mapObj);
});

$("#variables").change(function () {
    clearMap();
    layerObj = newLayer();
    controlsObj = makeControls();
    getChart(drawnItems);
    legend.addTo(mapObj);
});

$("#opacity").change(function () {
    layerObj.setOpacity($('#opacity').val());
});

$('#colors').change(function () {
    clearMap();
    layerObj = newLayer();
    controlsObj = makeControls();
    legend.addTo(mapObj);
});

$("#charttype").change(function () {
    if ($("#charttype").val() === 'singleline') {
        newSingleLinePlot(plotdata);
    } else if ($("#charttype").val() === 'multiline') {
        newMultiLinePlot(plotdata);
    } else if ($("#charttype").val() === 'boxplot') {
        newBoxWhiskerPlot(plotdata);
    }
});

$("#districtstats").click(function () {
    getShapeChart();
});