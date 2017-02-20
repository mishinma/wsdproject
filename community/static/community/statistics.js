
function set_overall_values(overall_revenue, games_sold) {
    'use strict';
    $('#overallRevenue').text(overall_revenue);
    $('#gamesSold').text(games_sold);
}


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
            },
            scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true,
                    stepSize: 1
                }
            }]
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

