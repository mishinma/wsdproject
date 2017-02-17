
function send_error_message (jqXHR, exception)  {
    // Send ERROR message
    'use strict';
    var msg = {
        "messageType": "ERROR",
        "info": jqXHR.responseText
    };
    var gameIframe = $("#playGameIframe")[0];
    gameIframe.contentWindow.postMessage(msg, gameIframe.src);
}


function update_scores (data) {
    'use strict';
    $("#userHighScore").text(data.userHighScore);
    $("#userLastScore").text(data.userLastScore);
    var topScores = data.top3_scores;
    $("#leaderList").text(topScores);
}


function load_game (data) {
    // Send LOAD message
    'use strict';
     var msg = {
         "messageType": "LOAD",
         "gameState": data
     };
     var gameIframe = $("#playGameIframe")[0];
     gameIframe.contentWindow.postMessage(msg, gameIframe.src);
}


// Communication between the game and the service using window.postMessage.
$(document).ready(function () {
    "use strict";
    window.addEventListener("message", function (evt) {

        switch (evt.data["messageType"]){

            case "SETTING":
                // ToDo: set options before the document is ready?
                var options = evt.data.options;
                options.visibility = 'visible';
                $("#playGameIframe").css(options);
                break;

            case "SCORE":
                $.ajax({
                    method: "POST",
                    data: evt.data,
                    dataType: 'json',
                    success: update_scores,
                    error: send_error_message
                });
                break;

            case "SAVE":
                var data = {
                    messageType: evt.data.messageType,
                    gameState: JSON.stringify(evt.data.gameState)
                };
                $.ajax({
                    method: "POST",
                    data: data,
                    error: send_error_message
                });
                break;

            case "LOAD_REQUEST":
                $.ajax({
                    method: "POST",
                    data: evt.data,
                    dataType: 'json',
                    success: load_game,
                    error: send_error_message
                });
                break;

            default:
                console.log('Unrecognized message type');
        }
    });
});