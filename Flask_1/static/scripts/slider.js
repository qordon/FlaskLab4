var dates = []
var temperatures = []
var ctx = document.getElementById('myChart').getContext('2d');
var chart;

Chart.defaults.global.defaultFontFamily = "Lato";
Chart.defaults.global.defaultFontSize = 18;

var chartOptions = {
  legend: {
    display: true,
    labels: {
      boxWidth: 80,
      fontColor: 'red'
    }
  }
};

function create_graphic()
{
    var temperatureData = {
    labels: dates,
    datasets: [{
    borderColor: "rgb(100,100,100)",
    backgroundColor: "rgb(0,255,255)",
    label: "Temperature (C)",
    data: temperatures,
     }]
    };

    chart = new Chart(ctx, {
      type: 'line',
      data: temperatureData,
      options: chartOptions
    });
}

function update_temperature()
{
    $.ajax({
            type: 'get',
            url: '/temperature/'
            })
            .done(function(data){
                if(dates.length == 0)
                {
                    temperatures = data["temperatures"];
                    dates = data["dates"];
                    create_graphic();
                }
                else
                {
                    chart.data.labels.splice(0,1);
                    chart.data.datasets[0].data.splice(0,1);

                    chart.data.labels.push(data["dates"][9]);
                    chart.data.datasets[0].data.push(data["temperatures"][9]);
                    chart.update();
                }

                if(data["heater_state"] == 1)
                {
                    console.log("IF");
                    $('#heater_mode').text("Подогрев включен");
                }
                else
                {
                    console.log("NOT IF");
                    $('#heater_mode').text("Подогрев выключен");
                }

                $('#t-hall').text(temperatures[temperatures.length - 1] +' C');
            });
    setTimeout(update_temperature,5000);
}

setTimeout(update_temperature,200);

function switchBulb(){
    bulb = document.getElementById('lamp');
    $.ajax({
            type: 'get',
            url: '/lamp'
        })
        .done(function(data){
            if(data['hall'] == false){
                bulb.src = '/static/images/bulb-on.png';
            }
            else{
                bulb.src = '/static/images/bulb.png';
            }
        });
}

function openbox(id){
    var display = document.getElementById(id).style.display;

    if(display=='none'){
       document.getElementById(id).style.display='block';
    }
    else{
       document.getElementById(id).style.display='none';
    }
}

function change_brightness(){
    slider = document.getElementById('myRange');
    place = document.getElementById('value-bright');
    place.innerHTML = "Освещение: " + slider.value + "%";

    $.ajax({
            type: 'get',
            url: '/brightness/' + slider.value
        })
        .done(function(){

        });
}

function apply_temperature_limits()
{
    min_temperature_limit = document.getElementById("min_temperature_entry").value;
    max_temperature_limit = document.getElementById("max_temperature_entry").value;

    if(min_temperature_limit == "")
    {
        min_temperature_limit = 0;
    }

     if(max_temperature_limit == "")
    {
        max_temperature_limit = 0;
    }

    $.ajax({
            type: 'get',
            url: '/set_temperature_limits/' + min_temperature_limit + "_" + max_temperature_limit
        })
        .done(function(){

        });
}



