var vibe_gauge_options = {
    angle: 0,
    lineWidth: 0.2,
    pointer: {
      length: 0.6,
      strokeWidth: 0.05,
      color: '#000000'
    },
    staticZones: [
       {strokeStyle: "#30B32D", min: 0, max: 1},
       {strokeStyle: "#FFDD00", min: 1, max: 10},
       {strokeStyle: "#F03E3E", min: 10, max: 15}
    ],
    limitMax: false,
    limitMin: false,
    strokeColor: '#E0E0E0',
    highDpiSupport: true
  };

$(function () {
    $("#update-interval").val(loadData);
    var target = document.getElementById('vibration');
    var vibe_gauge = new Gauge(target).setOptions(vibe_gauge_options);
    vibe_gauge.minValue = 0;
    vibe_gauge.maxValue = 15;
    vibe_gauge.setOptions(vibe_gauge_options);
    vibe_gauge.set(0);

    setInterval(function(){
	$.get("data.json", function (data) {
	    vibe_gauge.set(Math.min(15,data['vibration'])); //make sure gauge stays in bounds
	    $("#temperature").text(data['temperature'].toFixed(2))
	    $("#humidity").text(data['humidity'].toFixed(2))
        //change the humidity background to red if > 75%
        if(data['humidity']>75){
            $("#humidity-container").css("background","red")
        } else{
            $("#humidity-container").css("background","inherit")
        }
	});

    }, 2000);
    
}); 

function loadData(){
}


