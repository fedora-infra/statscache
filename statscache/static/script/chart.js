var pending = null; /* current pending request */
var loadingError =
    "An error occurred, and the content could not be loaded";
var feed = "http://localhost:5000/api/volume-by-category-1h";
var rows_per_page = 100;
var page = 1;
var order = 'desc';
var keys;
var template;

var margin = {
    top: 0,
    right: 0,
    bottom: 10,
    left: 0
};

width = 838 - margin.left - margin.right;
height = 300 - margin.top - margin.bottom;

var x = d3.scale.ordinal().rangeRoundBands([0, width], 0.1);

var y = d3.scale.linear().range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var chart = d3.select(".day_chart")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


function render_graph(data) {

    data.forEach(type);
    x.domain(data.map(function (d) {
        return d.timestamp;
    }));

    y.domain([0, d3.max(data, function (d) {
        return d.volume;
    })]);

    chart.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    chart.append("g")
        .attr("class", "y axis")
        .call(yAxis);

    chart.selectAll(".bar")
        .data(data)
        .enter().append("rect")
        .attr("class", "bar")
        .attr("x", function (d) {
            return x(d.timestamp);
        })
        .attr("y", function (d) {
            return y(d.volume);
        })
        .attr("height", function (d) {
            return height - y(d.volume);
        })
        .attr("width", x.rangeBand());

    console.log("DATA", data);

    function type(d) {
        d.volume = +d.volume; // coerce to number
        return d;
    }
}


function render(data) {
    if (page==1) {
        keys = Object.keys(data[0]);
        keys.splice(keys.indexOf('timestamp'), 1);
        keys.unshift('timestamp');
    }
    data.forEach(function (row) {
        t = new Date();
        t.setTime(row.timestamp*1000);
        row.timestamp = t.toUTCString();
        keys.forEach(function (key) {
            row[key] = String(row[key]).htmlEscape();
        });
    });
    render_graph(data)
}

function request() {
    if (pending) {
        return;
    }
    $('#loading').show();
    pending = $.ajax(
        feed + "?" + $.param(
            {
                'rows_per_page': rows_per_page,
                'page': page,
                'start': $('#start-datetime').data('DateTimePicker').date().format('X'),
                'stop': $('#stop-datetime').data('DateTimePicker').date().format('X'),
                'order': order,
            }
        ),
        {
            'dataType': 'json',
            'complete': function (request, status) {
                pending = null;
            },
            'error': function (request, status, error) {
                console.log("error: " + status);
            },
            'success': function (response, status, request) {
                render(response);
                ++page;
            }
        }
    );
}

function reload() {
    if (pending) {
        pending.abort();
    }
    $('thead.stats,tbody.stats,tfoot.stats').html("");
    page = 1;
    request();
}

$(function () {
    $('#chose-ascending').on('click', function (e) {
        if (order == 'asc') {
            return;
        }
        $('#ordering-menu').text("ascending");
        order = 'asc';
        reload();
    });
    $('#chose-descending').on('click', function (e) {
        if (order == 'desc') {
            return;
        }
        order = 'desc';
        $('#ordering-menu').text("descending");
        reload();
    });

    $('.datetimepicker').datetimepicker();

    // FIXME
    epoch = 1438972200.0
    now = 1498497519.29
    epoch = moment(epoch + 60 - (epoch % 60), "X");
    now = moment(now - (now % 60), "X");

    $('#start-datetime').data('DateTimePicker').minDate(epoch);
    $('#start-datetime').data('DateTimePicker').maxDate(now);
    $('#start-datetime').data('DateTimePicker').defaultDate(epoch);
    $('#start-datetime').on('dp.change', function (e) {
        /* ensure that the stop datetime won't precede the new start */
        $('#stop-datetime').data('DateTimePicker').minDate(
            $('#start-datetime').data('DateTimePicker').date()
        );
    });

    $('#stop-datetime').data('DateTimePicker').minDate(epoch);
    $('#stop-datetime').data('DateTimePicker').maxDate(now);
    $('#stop-datetime').data('DateTimePicker').defaultDate(now);
    $('#stop-datetime').on('dp.change', function (e) {
        /* ensure that the start datetime won't succeed the new stop */
        $('#start-datetime').data('DateTimePicker').maxDate(
            $('#stop-datetime').data('DateTimePicker').date()
        );
    });

    $('.datetimepicker').on('dp.change', reload);

    /* load initial (default) content */
    $('#loading').on('appear', request);
    $('#loading').appear();
    $('#loading').trigger('appear');
});
