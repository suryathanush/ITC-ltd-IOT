
var host = "http://localhost/IotDashboard/";
var apiHost = "http://103.10.133.104:8081/api_noauth/";
var authorizationToken = "851c6154b0b590c97c53af318195787eeba3a690";
var registerApiInterval = 5000;
var dataApiInterval = 10000;
var timeIntervalForDataApi = 5;
var apiSensorKey = null;
var apiDataArray = null;

$(window).on("load", function () {
    $("#tblPageHeader").attr("width", (window.innerWidth - 30));
    $("#imgLogo").attr("src", host + 'Image/Logo.png');
    $(".waiter-spn").css("top", "200px");
    $(".waiter-spn").css("left", ((window.innerWidth - $(".waiter-spn").css("width").replace("px", "")) / 2) + "px");
    $("#divTimeIntervalLabel").html("Time interval is " + timeIntervalForDataApi + ". Please change if you want...");
    document.getElementById("rngTimeInterval").oninput = function () {
        $("#divTimeIntervalLabel").html("Time interval is " + this.value + ". Please change if you want...");
    };
    document.getElementById("rngTimeInterval").onchange = function () {
        $(this).attr("title", this.value);
        timeIntervalForDataApi = this.value;
        $("#divTimeIntervalLabel").html("Time interval is " + timeIntervalForDataApi + ". Please change if you want...");
        drawGraphs();
    };

    registerForAPI();
    setInterval(registerForAPI, registerApiInterval);
    setInterval(drawGraphs, dataApiInterval);
});

function registerForAPI() {
    $.ajax({
        type: "GET",
        contentType: "application/json",
        dataType: "json",
        url: apiHost + "register_card/",
        async: true,
        headers: {
            "Authorization": authorizationToken
        },
        success: function (data) {
            if (data != null) {
                $("#divSensorButtons").html("");
                $.each(data, function (key, value) {
                    $("#divSensorButtons").html(
                        $("#divSensorButtons").html() +
                        "<div id='" + key + "' onclick='callDrawGraphs(\"" + key + "\")'" +
                        " class='sensor-spn-outer'><div class='sensor-spn-inner'>" + key +
                        "<br /><span class='sensor-spn-inner-value'>Total active energy : " + value + "</span></div></div>"
                    );
                    if (apiSensorKey == null || apiSensorKey == undefined) {
                        apiSensorKey = key;
                        drawGraphs();
                    }
                });
            }
        }
    });
}

function callDrawGraphs(sensorKey) {
    apiSensorKey = sensorKey;
    drawGraphs();
}

function drawGraphs() {
    if (apiSensorKey != null && apiSensorKey != undefined) {
        $(".waiter-spn").css("display", "block");
        $("#graphIaIbIcIavg").html("");
        $("#graphVabVbcVcaVavg").html("");
        $("#graphVanVbnVcnVavg").html("");
        $("#graphPowaPowbPowcPowtot").html("");
        $("#graphPfaPfbPfcPftot").html("");
        $("#graphFrequency").html("");
        $(".graph-spn-title").css("display", "none");
        $.ajax({
            type: "GET",
            contentType: "application/json",
            dataType: "json",
            async: true,
            url: apiHost + "register_graph/?register=" + apiSensorKey + "&time_interval=" + timeIntervalForDataApi + "",
            success: function (dataArr) {
                apiDataArray = dataArr;
                google.charts.load('current', { 'packages': ['line'] });
                google.charts.setOnLoadCallback(drawGraphIaIbIcIavg);
                google.charts.setOnLoadCallback(drawGraphVabVbcVcaVavg);
                google.charts.setOnLoadCallback(drawGraphVanVbnVcnVavg);
                google.charts.setOnLoadCallback(drawGraphPowaPowbPowcPowtot);
                google.charts.setOnLoadCallback(drawGraphPfaPfbPfcPftot);
                google.charts.setOnLoadCallback(drawGraphfrequency);
                $(".graph-spn-title").css("width", (window.innerWidth - 54) + "px");
                $(".graph-spn-title").css("display", "block");
                $(".waiter-spn").css("display", "none");
            }
        });
    }
}

function drawGraphIaIbIcIavg() {
    if (apiDataArray.length > 0) {
        var data = new google.visualization.DataTable();

        data.addColumn('datetime', 'Date & Time');
        data.addColumn('number', 'i_a');
        data.addColumn('number', 'i_b');
        data.addColumn('number', 'i_c');
        data.addColumn('number', 'i_avg');

        $.each(apiDataArray, function (key, value) {
            data.addRows([
                [new Date(value.timestamp), value.i_a, value.i_b, value.i_c, value.i_avg]
            ]);
        });

        var options = {
            chart: {
                title: '',
                subtitle: ''
            },
            titlePosition: 'none',
            hAxis: {
                format: 'yy/MM/dd hh:mm:ss',
            },
            width: (window.innerWidth - 50),
            height: 400,
            backgroundColor: 'lightblue',
        };

        var chart = new google.charts.Line(document.getElementById('graphIaIbIcIavg'));
        chart.draw(data, google.charts.Line.convertOptions(options));
    }
    else {
        document.getElementById('graphIaIbIcIavg').innerHTML =
            "<div class='graph-spn-no-data-outer'>" +
            "<div class='graph-spn-no-data-inner'>" +
            "Graph i_a, i_b, i_c, i_avg <br /> <br /> Oooops! No Data!" +
            "</div ></div > ";
    }
}

function drawGraphVabVbcVcaVavg() {
    if (apiDataArray.length > 0) {
        var data = new google.visualization.DataTable();

        data.addColumn('datetime', 'Date & Time');
        data.addColumn('number', 'v_ab');
        data.addColumn('number', 'v_bc');
        data.addColumn('number', 'v_ca');
        data.addColumn('number', 'v_ll_avg');

        $.each(apiDataArray, function (key, value) {
            data.addRows([
                [new Date(value.timestamp), value.v_ab, value.v_bc, value.v_ca, value.v_ll_avg]
            ]);
        });

        var options = {
            chart: {
                title: '',
                subtitle: ''
            },
            hAxis: {
                format: 'yy/MM/dd hh:mm:ss',
            },
            width: (window.innerWidth - 50),
            height: 400,
            backgroundColor: 'lightblue',
        };

        var chart = new google.charts.Line(document.getElementById('graphVabVbcVcaVavg'));
        chart.draw(data, google.charts.Line.convertOptions(options));
    }
    else {
        document.getElementById('graphVabVbcVcaVavg').innerHTML =
            "<div class='graph-spn-no-data-outer'>" +
            "<div class='graph-spn-no-data-inner'>" +
            "Graph v_ab, v_bc, v_ca, v_ll_avg <br /> <br /> Oooops! No Data!" +
            "</div ></div > ";
    }
}

function drawGraphVanVbnVcnVavg() {
    if (apiDataArray.length > 0) {
        var data = new google.visualization.DataTable();

        data.addColumn('datetime', 'Date & Time');
        data.addColumn('number', 'v_an');
        data.addColumn('number', 'v_bn');
        data.addColumn('number', 'v_cn');
        data.addColumn('number', 'v_ln_avg');

        $.each(apiDataArray, function (key, value) {
            data.addRows([
                [new Date(value.timestamp), value.v_an, value.v_bn, value.v_cn, value.v_ln_avg]
            ]);
        });

        var options = {
            chart: {
                title: '',
                subtitle: ''
            },
            hAxis: {
                format: 'yy/MM/dd hh:mm:ss',
            },
            width: (window.innerWidth - 50),
            height: 400,
            backgroundColor: 'lightblue',
        };

        var chart = new google.charts.Line(document.getElementById('graphVanVbnVcnVavg'));
        chart.draw(data, google.charts.Line.convertOptions(options));
    }
    else {
        document.getElementById('graphVanVbnVcnVavg').innerHTML =
            "<div class='graph-spn-no-data-outer'>" +
            "<div class='graph-spn-no-data-inner'>" +
            "Graph v_an, v_bn, v_cn, v_ln_avg <br /> <br /> Oooops! No Data!" +
            "</div ></div > ";
    }
}

function drawGraphPowaPowbPowcPowtot() {
    if (apiDataArray.length > 0) {
        var data = new google.visualization.DataTable();

        data.addColumn('datetime', 'Date & Time');
        data.addColumn('number', 'active_pow_a');
        data.addColumn('number', 'active_pow_b');
        data.addColumn('number', 'active_pow_c');
        data.addColumn('number', 'active_power_tot');

        $.each(apiDataArray, function (key, value) {
            data.addRows([
                [new Date(value.timestamp), value.active_pow_a, value.active_pow_b, value.active_pow_c, value.active_power_tot]
            ]);
        });

        var options = {
            chart: {
                title: '',
                subtitle: ''
            },
            hAxis: {
                format: 'yy/MM/dd hh:mm:ss',
            },
            width: (window.innerWidth - 50),
            height: 400,
            backgroundColor: 'lightblue',
        };

        var chart = new google.charts.Line(document.getElementById('graphPowaPowbPowcPowtot'));
        chart.draw(data, google.charts.Line.convertOptions(options));
    }
    else {
        document.getElementById('graphPowaPowbPowcPowtot').innerHTML =
            "<div class='graph-spn-no-data-outer'>" +
            "<div class='graph-spn-no-data-inner'>" +
            "Graph active_pow_a, active_pow_b, active_pow_c, active_power_tot <br /> <br /> Oooops! No Data!" +
            "</div ></div > ";
    }
}

function drawGraphPfaPfbPfcPftot() {
    if (apiDataArray.length > 0) {
        var data = new google.visualization.DataTable();

        data.addColumn('datetime', 'Date & Time');
        data.addColumn('number', 'pf_a');
        data.addColumn('number', 'pf_b');
        data.addColumn('number', 'pf_c');
        data.addColumn('number', 'pf_tot');

        $.each(apiDataArray, function (key, value) {
            data.addRows([
                [new Date(value.timestamp), value.pf_a, value.pf_b, value.pf_c, value.pf_tot]
            ]);
        });

        var options = {
            chart: {
                title: '',
                subtitle: ''
            },
            hAxis: {
                format: 'yy/MM/dd hh:mm:ss',
            },
            width: (window.innerWidth - 50),
            height: 400,
            backgroundColor: 'lightblue',
        };

        var chart = new google.charts.Line(document.getElementById('graphPfaPfbPfcPftot'));
        chart.draw(data, google.charts.Line.convertOptions(options));
    }
    else {
        document.getElementById('graphPfaPfbPfcPftot').innerHTML =
            "<div class='graph-spn-no-data-outer'>" +
            "<div class='graph-spn-no-data-inner'>" +
            "Graph pf_a, pf_b, pf_c, pf_tot <br /> <br /> Oooops! No Data!" +
            "</div ></div > ";
    }
}

function drawGraphfrequency() {
    if (apiDataArray.length > 0) {
        var data = new google.visualization.DataTable();

        data.addColumn('datetime', 'Date & Time');
        data.addColumn('number', 'Frequency');

        $.each(apiDataArray, function (key, value) {
            data.addRows([
                [new Date(value.timestamp), value.frequency]
            ]);
        });

        var options = {
            chart: {
                title: '',
                subtitle: ''
            },
            hAxis: {
                format: 'yy/MM/dd hh:mm:ss',
            },
            width: (window.innerWidth - 50),
            height: 400,
            backgroundColor: 'lightblue',
        };

        var chart = new google.charts.Line(document.getElementById('graphFrequency'));
        chart.draw(data, google.charts.Line.convertOptions(options));
    }
    else {
        document.getElementById('graphFrequency').innerHTML =
            "<div class='graph-spn-no-data-outer'>" +
            "<div class='graph-spn-no-data-inner'>" +
            "Graph thd_i_a, thd_i_b, thd_i_c <br /> <br /> Oooops! No Data!" +
            "</div ></div > ";
    }
}