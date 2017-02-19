
function plot_games_sold_month(data){
    'use strict';
    console.log(data.months);
    console.log('fuck');
    var plot_data = {
        labels: data.months,
        datasets: [
            {
                label: 'Number of purchases',
                data: data.num_purchases
            }
        ]
    };
    var ctx = document.getElementById("allGamesSoldMonth");
    var myLineChart = new Chart(ctx, {
        type: 'line',
        data: plot_data,
        options: {
            title: {
                display: true,
                text: 'Games sold per month',
                fontSize: 18
            },
            legend: {
                display: false
            }
        }
    });
}

$(document).ready(function () {
    "use strict";
    $.ajax({
        method: "GET",
        dataType: 'json',
        success: plot_games_sold_month
    });

});