// Global Highcharts options
Highcharts.setOptions({
    lang: {
        downloadCSV: "Download CSV",
        downloadJPEG: "Download JPEG image",
        downloadPDF: "Download PDF document",
        downloadPNG: "Download PNG image",
        downloadSVG: "Download SVG vector image",
        downloadXLS: "Download XLS",
        loading: "Timeseries loading, please wait...",
        noData: "No Data Selected. Place a point, draw a polygon, or select a region."
    },
});

let chartdata = null;

// Placeholder chart
let chart = Highcharts.chart('highchart', {
    title: {
        align: "center",
        text: "Timeseries Data Chart Placeholder",
    },
    series: [{
        data: [],
    }],
    chart: {
        animation: true,
        zoomType: 'x',
        borderColor: '#000000',
        borderWidth: 2,
        type: 'area',
    },
    noData: {
        style: {
            fontWeight: 'bold',
            fontSize: '15px',
            color: '#303030'
        }
    },
});

function newHighchart(data) {
    chart = Highcharts.chart('highchart', {
        title: {
            align: "center",
            text: data['name'] + ' v Time ' + '(' + data['type'] + ')',
        },
        xAxis: {
            type: 'datetime',
            title: {text: "Time"},
        },
        yAxis: {
            title: {text: data['units']}
        },
        series: [{
            data: data['singleline'],
            type: "line",
            name: data['name'],
            tooltip: {
                xDateFormat: '%A, %b %e, %Y',
            },
        }],
        chart: {
            animation: true,
            zoomType: 'xy',
            borderColor: '#000000',
            borderWidth: 2,
            type: 'area',

        },

    });
}

function newMultilineChart(data) {
    let charttype = $("#charttype").val();
    chart = Highcharts.chart('highchart', {
        title: {
            align: "center",
            text: data['name'] + ' v Time ' + '(' + data['type'] + ') (stats for all ensembles)',
        },
        xAxis: {
            title: {text: "Time"},
        },
        yAxis: {
            title: {text: data['units']}
        },
        series: [
            {
                data: data['multiline']['min'],
                type: "line",
                name: 'Yearly Minimum',
            },
            {
                data: data['multiline']['max'],
                type: "line",
                name: 'Yearly Maximum',
            },
            {
                data: data['multiline']['mean'],
                type: "line",
                name: 'Yearly Average',
            }
        ],
        chart: {
            animation: true,
            zoomType: 'xy',
            borderColor: '#000000',
            borderWidth: 2,
            type: 'area',

        },

    });
}

function newBoxPlot(data) {
    let charttype = $("#charttype").val();
    chart = Highcharts.chart('highchart', {
        chart: {
            type: 'boxplot',
            animation: true,
            zoomType: 'xy',
            borderColor: '#000000',
            borderWidth: 2,
        },
        title: {align: "center", text: data['name'] + ' Statistics ' + '(' + data['type'] + ') (stats for all ensembles)'},
        legend: {enabled: false},
        xAxis: {
            title: {text: 'Time'},
            // categories: data['categories'],
        },
        yAxis: {title: {text: data['units']}},
        series: [{
            name: data['name'],
            data: data['boxplot'],
            tooltip: {xDateFormat: '%b',},
        }]

    });
}

function getDrawnChart(drawnItems) {
    // if there's nothing to get charts for then quit
    let geojson = drawnItems.toGeoJSON()['features'];
    if (geojson.length === 0 && currentregion === '') {
        return
    }

    // if there's geojson data, update that chart
    if (geojson.length > 0) {
        chart.hideNoData();
        chart.showLoading();

        //  Compatibility if user picks something out of normal bounds
        let coords = geojson[0]['geometry']['coordinates'];
        for (let i in coords.length) {
            if (coords[i] < -180) {
                coords[i] += 360;
            }
            if (coords[i] > 180) {
                coords[i] -= 360;
            }
        }

        // setup a parameters json to generate the right timeserie
        let data = {
            coords: coords,
            variable: $("#variables").val(),
            ensemble: $("#ensemble").val(),
            anominterval: $("#anominterval").val(),
            loc_type: geojson[0]['geometry']['type']
        };

        // decide which ajax url you need based on drawing type
        $.ajax({
            url: '/apps/' + app + '/ajax/getChart/',
            data: JSON.stringify(data),
            dataType: 'json',
            contentType: "application/json",
            method: 'POST',
            success: function (result) {
                chartdata = result;
                makechart();
            }
        })
        // If there isn't any geojson, then you actually should refresh the shapefile chart (ie the data is the lastregion)
    } else {
        getShapeChart('lastregion');
    }
}

function getShapeChart(selectedregion) {
    // if the time range is all times then confirm before executing the spatial averaging
    if ($("#dates").val() === 'alltimes') {
        if (!confirm("Computing a timeseries of spatial averages for all available times requires over 200 iterations of file conversions and geoprocessing operations. This may result in a long wait (15+ seconds) or cause errors. Are you sure you want to continue?")) {
            return
        }
    }

    drawnItems.clearLayers();
    chart.hideNoData();
    chart.showLoading();

    // setup a parameters json to generate the right timeseries
    let data = {
        variable: $("#variables").val(),
        ensemble: $("#ensemble").val(),
        anominterval: $("#anominterval").val(),
        loc_type: 'Shapefile'
    };

    if (selectedregion === 'lastregion') {
        // if we want to update, change the region to the last completed region
        data['region'] = currentregion;
    } else if (selectedregion === 'customshape') {
        data['region'] = selectedregion;
        currentregion = selectedregion;
    } else {
        // otherwise, the new selection is the current region on the chart
        data['region'] = selectedregion;
        currentregion = selectedregion;
    }

    $.ajax({
        url: '/apps/' + app + '/ajax/getChart/',
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: "application/json",
        method: 'POST',
        success: function (result) {
            chartdata = result;
            makechart();
        }
    })
}

function makechart() {
    if (chartdata !== null) {
        let type = $("#charttype").val();
        if (type === 'singleline') {
            newHighchart(chartdata);
        } else if (type === 'multiline') {
            newMultilineChart(chartdata);
        } else if (type === 'boxplot') {
            newBoxPlot(chartdata);
        }
    }
}
