
// Communication between the game and the service using window.postMessage.
$(document).ready(function () {
    "use strict";
    window.addEventListener("message", function (evt) {

        switch (evt.data["messageType"]){
            // ToDo: set options before the document is ready?
            case "SETTING":
                var options = evt.data.options;
                options.visibility = 'visible';
                $("#playGameIframe").css(options);
                break;
            case "SCORE":
                $.ajax({
                    method: "POST",
                    data: evt.data,
                    success: function (data) {
                        $("#userHighScore").text(data.userHighScore);
                        $("#userLastScore").text(data.userLastScore);
                    }
                });
                break;
            default:
                console.log('Unrecognized message type');
        }
    });
});