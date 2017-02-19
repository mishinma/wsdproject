
function plot_games_sold_month(data){
    'use strict';
    console.log(data.months);
    console.log('fuck');
    var plot_data = {
        labels: data.months,
        datasets: [
            {
                label: "Games sold per month",
                data: data.num_purchases
            }
        ]
    };
    var ctx = document.getElementById("allGamesSoldMonth");
    var myLineChart = new Chart(ctx, {
        type: 'line',
        data: plot_data
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