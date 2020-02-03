function getDomain() {
    var url = window.location.href;
    var arr = url.split("/");
    var result = arr[0] + "//" + arr[2];
    return result;
}

function saveStates(gameState) {
    var destination = getDomain() + "/webshop/savegame/";
    $.ajax({
        url: destination,
        type: "GET",
        data: {
            gameID: gameID,
            gameState: gameState
        },
        success: function (json) {
            console.log("saved");
        }
    });
}

function loadStates() {
    var destination = getDomain() + "/webshop/loadgame/";
    $.ajax({
        url: destination,
        type: "GET",
        data: {
            gameID: gameID
    },
        success: function (json) {
            var gameState = JSON.parse(json);
            var msg = {};
            msg.messageType = "LOAD";
            msg.gameState = gameState;
            var frame = document.getElementById('gameframe');
            frame.contentWindow.postMessage(msg, "*");
            console.log("loaded");
        }
    });
}

/* global $ */
$(document).ready(function () {
    'use strict';
    window.addEventListener('message', function (evt) {
        //Note that messages from all origins are accepted
        //Get data from sent message
        var data = evt.data;

        if (data.messageType == "SETTING") {
            $('iframe').width(data.options.width);
            $('iframe').height(data.options.height);
        };

        if (data.messageType == "SCORE") {
            $('#score').empty();
            $('#score').append(data.score);
        };

        if (data.messageType == "SAVE") {
            var gameState = JSON.stringify(data.gameState);
            console.log(gameState)
            saveStates(gameState)
            $('#actions').empty();
            $('#actions').append("Saved");
        };

        if (data.messageType == "LOAD_REQUEST") {
            /*if (NO SAVED GAMESTATE) {
              $('#actions').empty();
              $('#actions').append("No game state saved - could not load");
            }
            else {*/
            loadStates();
            $('#actions').empty();
            $('#actions').append("Loaded");
            //}
        };
    });
});

