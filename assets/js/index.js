$(function () {
    setInterval(loadData, 2000);
    $("#update-interval").val(loadData);
});

function loadData(){
    $.get("data.json", function (data) {
        $("#data").text("Lat: "+data['lat']+" Long: "+data['long']);
    });
}


