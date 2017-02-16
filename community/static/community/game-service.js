
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
                    success: function (data) {
                        $("#userHighScore").text(data.userHighScore);
                        $("#userLastScore").text(data.userLastScore);
                    },
                    error: function (jqXHR, exception) {
                        // Bad message
                        console.log(jqXHR.responseText);
                    }
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
                    success: function () {
                        console.log('State saved')
                    },
                    error: function (jqXHR, exception) {
                        // Bad message
                        console.log(jqXHR.responseText);
                    }
                });
                break;

            default:
                console.log('Unrecognized message type');
        }
    });
});