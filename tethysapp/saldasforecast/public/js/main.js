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
function getThreddswms() {
    $.ajax({
        url: '/apps/saldasforecast/ajax/customsettings/',
        async: false,
        data: '',
        dataType: 'json',
        contentType: "application/json",
        method: 'POST',
        success: function (result) {
            wmsbase = result['threddsurl'];
        },
    });
}

let wmsbase;
getThreddswms();                        // sets the value of wmsbase
const mapObj = map();                   // used by legend and draw controls
const basemapObj = basemaps();          // used in the make controls function

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

////////////////////////////////////////////////////////////////////////  CREATE/ADD LEGEND
let legend = L.control({position: 'bottomright'});
legend.onAdd = function (mapObj) {
    let div = L.DomUtil.create('div', 'legend');
    let url;
    if ($("#anomaly").val() === 'ensemble_mean') {
        url =  wmsbase + $("#anomaly").val() + '.ncml';
    } else {
        url = wmsbase + $("#anomaly").val() + $("#ensemble").val();
    }
    url = url + "?REQUEST=GetLegendGraphic&LAYER=" + $("#variables").val() + "&PALETTE=" + $('#colors').val() + "&COLORSCALERANGE=-15,15";
    div.innerHTML = '<img src="' + url + '" alt="legend" style="width:100%; float:right;">';
    return div
};
legend.addTo(mapObj);


////////////////////////////////////////////////////////////////////////  EVENT LISTENERS

//  Listener for the variable picker menu (selectinput gizmo)
$("#anomaly").change(function (self) {
    clearMap();
    layerObj = newLayer();
    controlsObj = makeControls();
    getChart(drawnItems);
    legend.addTo(mapObj);
    if ($("#anomaly").val() === 'ensemble_mean') {
        $("#box-warning").show();
    } else {
        $("#box-warning").hide();
    }
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

