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
    minValue: -90,
    maxValue: 90,
    colorStart: '#E0E0E0',   // Colors
    colorStop: '#E0E0E0',    // just experiment with them
    strokeColor: '#E0E0E0',  // to see which ones work best for you
    generateGradient: true,
    highDpiSupport: true,     // High resolution support
    
};

$(function () {
    $("#update-interval").val(loadData);
    var target = document.getElementById('roll');
    var roll = new Gauge(target).setOptions(gauge_opts);
    setInterval(function(){
	$.get("data.json", function (data) {
	    roll.set(data['roll'])
	    $("#temperature").text(data['temperature'].toFixed(2))
	    $("#humidity").text(data['humidity'].toFixed(2))
	});

    }, 2000);
    
}); 

function loadData(){
}


