
function plot_games_sold_month(months, num_purchases){
    'use strict';

    var plot = {
        labels: months,
        datasets: [
            {
                label: 'Number of purchases',
                data: num_purchases
            }
        ]
    };

    var ctx = document.getElementById("allGamesSoldMonth");

    var myLineChart = new Chart(ctx, {
        type: 'line',
        data: plot,
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


function plot_revenue_per_game(game_names, revenues){
    'use strict';

    var data = {
        labels: game_names,
        datasets: [
            {
                label: 'Number of purchases',
                data: revenues
            }
        ]
    };

    var ctx = document.getElementById("allRevenuePerGame");

    var myBarChart = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            title: {
                display: true,
                text: 'Revenue per game',
                fontSize: 18
            },
            legend: {
                display: false
            },
            scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
        }
    });
}

$(document).ready(function () {
    "use strict";
    $.ajax({
        method: "GET",
        dataType: 'json',
        success: function (data) {
            $('#overallRevenue').text(data.overall_revenue);
            $('#gamesSold').text(data.games_sold);
            plot_games_sold_month(data.purchases_per_month_months,
                data.purchases_per_month_num_purchases);
            plot_revenue_per_game(data.revenue_per_game_game_names,
                data.revenue_per_game_revenues)
        }
    });


});