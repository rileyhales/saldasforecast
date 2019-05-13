// Global Highcharts options
Highcharts.setOptions({
    lang: {
        downloadCSV: "Download CSV",
        downloadJPEG: "Download JPEG image",
        downloadPDF: "Download PDF document",
        downloadPNG: "Download PNG image",
        downloadSVG: "Download SVG vector image",
        downloadXLS: "Download XLS",
        loading: "Loading timeseries, please wait...",
        noData: "No Data Selected"
    },
});

let plotdata;
let chart;

// Placeholder chart
chart = Highcharts.chart('highchart', {
    title: {
        align: "center",
        text: "Your Chart Will Appear Here",
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


function newSingleLinePlot(data) {
    chart = Highcharts.chart('highchart', {
        chart: {
            type: 'area',
            animation: true,
            zoomType: 'x',
            borderColor: '#000000',
            borderWidth: 2,
        },
        title: {align: "center", text: 'Forecasted ' + data['anominterval'] + ' ' + data['name'] + ' v Time'},
        xAxis: {
            type: 'datetime',
            title: {text: "Time"},
        },
        yAxis: {title: {text: data['units']}},
        series: [{
            data: data['singleline'],
            type: "line",
            name: data['name'],
            tooltip: {xDateFormat: '%A, %b %e, %Y'},
        }],

    });
}


function newMultiLinePlot(data) {
    chart = Highcharts.chart('highchart', {
        chart: {
            type: 'line',
            animation: true,
            zoomType: 'x',
            borderColor: '#000000',
            borderWidth: 2,
        },
        title: {align: "center", text: 'Forecasted ' + data['anominterval'] + ' ' + data['name'] + ' v Time'},
        xAxis: {
            type: 'datetime',
            title: {text: "Time"},
        },
        yAxis: {title: {text: data['units']}},
        series: [
            {
                data: data['multiline']['min'],
                type: "line",
                name: 'Forecast Minimum',
                tooltip: {xDateFormat: '%A, %b %e, %Y'},
            },
            {
                data: data['multiline']['max'],
                type: "line",
                name: 'Forecast Maximum',
                tooltip: {xDateFormat: '%A, %b %e, %Y'},
            },
            {
                data: data['multiline']['mean'],
                type: "line",
                name: 'Forecast Average',
                tooltip: {xDateFormat: '%A, %b %e, %Y'},
            }
        ],

    });
}


function newBoxWhiskerPlot(data) {
    chart = Highcharts.chart('highchart', {
        chart: {
            type: 'boxplot',
            animation: true,
            zoomType: 'x',
            borderColor: '#000000',
            borderWidth: 2,
        },
        title: {align: "center", text: 'Forecasted ' + data['anominterval'] + ' ' + data['name'] + ' v Time'},
        legend: {enabled: false},
        xAxis: {
            type: 'datetime',
            // categories: ['1', '2', '3', '4', '5'],
            title: {text: 'Time',}
        },
        yAxis: {title: {text: data['units']}},
        series: [{
            name: data['name'],
            data: data['boxplot'],
            tooltip: {xDateFormat: '%A, %b %e, %Y',},
        }]

    });
}


function getChart(drawnItems) {
//  Compatibility if user picks something out of normal bounds
    let geometry = drawnItems.toGeoJSON()['features'];
    if (geometry.length > 0) {
        chart.hideNoData();
        chart.showLoading();

        let coords = geometry[0]['geometry']['coordinates'];
        if (coords[0] < -180) {
            coords[0] += 360;
        }
        if (coords[0] > 180) {
            coords[0] -= 360;
        }

        let data = {
            coords: coords,
            variable: $('#variables').val(),
            anominterval: $("#anominterval").val(),
            ensemble: $("#ensemble").val(),
        };

        $.ajax({
            url: '/apps/saldasforecast/ajax/timeseriesplot/',
            data: JSON.stringify(data),
            dataType: 'json',
            contentType: "application/json",
            method: 'POST',
            success: function (result) {
                plotdata = result;
                let charttype = $("#charttype").val();
                if (charttype === 'singleline') {
                    newSingleLinePlot(plotdata);
                } else if (charttype === 'multiline') {
                    newMultiLinePlot(plotdata);
                } else if (charttype === 'boxplot') {
                    newBoxWhiskerPlot(plotdata);
                }
            }
        });
    }

}

function getShapeChart() {
    chart.hideNoData();
    chart.showLoading();
    let data = {
        variable: $('#variables').val(),
        anominterval: $("#anominterval").val(),
        shapefile: 'true',
        region: $("#regions").val(),
    };
    $.ajax({
        url: '/apps/gldas/ajax/getSpatialAverage/',
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: "application/json",
        method: 'POST',
        success: function (result) {
            console.log(result);
            newHighchart(result);
        }
    })
}
