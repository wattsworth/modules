var gauge_opts = {
    angle: 0.15, // The span of the gauge arc
    lineWidth: 0.44, // The line thickness
    radiusScale: 1, // Relative radius
    pointer: {
	length: 0.6, // // Relative to gauge radius
	strokeWidth: 0.035, // The thickness
	color: '#000000' // Fill color
    },
    limitMax: true,
    limitMin: true,
    minValue: 0,
    maxValue: 5,
    colorStart: '#6FADCF',   // Colors
    colorStop: '#8FC0DA',    // just experiment with them
    strokeColor: '#E0E0E0',  // to see which ones work best for you
    generateGradient: true,
    highDpiSupport: true,     // High resolution support
    
};

$(function () {
    $("#update-interval").val(loadData);
    var target = document.getElementById('knob1');
    var knob1 = new Gauge(target).setOptions(gauge_opts);
    knob1.maxValue=5;
    target = document.getElementById('knob2');
    var knob2 = new Gauge(target).setOptions(gauge_opts);
    knob2.maxValue=5;
    setInterval(function(){
	$.get("data.json", function (data) {
	    knob1.set(data['knob1'])
	    knob2.set(data['knob2'])
	    $("#lat").text(data['lat'].toFixed(2))
	    $("#long").text(data['long'].toFixed(2))
	});

    }, 2000);
    
}); 

function loadData(){
}


