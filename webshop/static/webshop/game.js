function domain() {
    return document.location.origin;
}

function error(error_info) {
    var message={};
    message.messageType ="ERROR";
    message.info = error_info;
    var frame = document.getElementById('gameframe');
    frame.contentWindow.postMessage(msg, "*");
}

// From https://docs.djangoproject.com/en/3.0/ref/csrf/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function saveStates(gameState) {
    // Saving the current gamestate with an ajax POST request
    var destination = domain() + "/webshop/savegame/";
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: destination,
        type: "POST",
        data: {
            gameID: gameID,
            gameState: gameState,
            csrfmiddlewaretoken: csrftoken
        },
        success: function (json) {
            alert("Your gamestate was saved!")
        },
        error: function(jqXHR,exception) {
            error(jqXHR.responseText);
        }
    });
}

function loadStates() {
    // Attempting to load a previously saved gamestate for this user in this game
    var destination = domain() + "/webshop/loadgame/";
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: destination,
        type: "POST",
        data: {
            gameID: gameID,
            csrfmiddlewaretoken: csrftoken
        },
        success: function (json) {
            if (json) {
                var gameState = JSON.parse(json);
                var msg = {};
                msg.messageType = "LOAD";
                msg.gameState = gameState;
                var frame = document.getElementById('gameframe');
                frame.contentWindow.postMessage(msg, "*");
                alert("Your gamestate was loaded successfully!")
            }
            else {
                // If no saved gamestate is found
                var gameState = JSON.parse(json);
                var msg = {};
                msg.messageType = "ERROR";
                msg.gameState = gameState;
                var frame = document.getElementById('gameframe');
                frame.contentWindow.postMessage(msg, "*");
                alert("No saved gamestate found - could not load")
            }
        },
        error: function(jqXHR,exception) {
            error(jqXHR.responseText);
        }
    });
}

function saveScore(score) {
    // Saving the user's current score with an ajax POST request
    var destination = domain() + "/webshop/savescore/";
    var csrftoken = getCookie('csrftoken');

    $.ajax({
        url: destination,
        type: "POST",
        data: {
            gameID: gameID,
            score: score,
            csrfmiddlewaretoken: csrftoken
        },
        success: function (json) {
            $('#score').empty();
            $('#score').append(score);
            alert("Score saved successfully!")
        },
        error: function(jqXHR,exception) {
            error(jqXHR.responseText);
        }
    });
}

function showHighscores() {
    // Fetching the top 10 scores of this game from the database with an ajax GET request
    var destination = domain() + "/webshop/highscore/";
    $.ajax({
        url: destination,
        type: "GET",
        data: {
            gameID: gameID
        },
        success: function (json) {
            if (json) {
                // Adding the top 10's users and scores to a list
                top10data = JSON.parse(json)
                $('#highscores').empty();
                $.each(top10data, function () {
                    var user = this.fields.user;
                    var score = this.fields.score;
                    var listItem = '\n\t<li>' + user + ": " + score + '</li>';
                    $('#highscores').append(listItem);
                });
            }
        },
        error: function(jqXHR,exception) {
            error(jqXHR.responseText);
        }
    });
}

$(document).ready(function () { updateHighscore(); });
// Updating global highscore list every 10 seconds
function updateHighscore() {
    showHighscores();
    setTimeout(updateHighscore, 10000);
}

/* global $ */
$(document).ready(function () {
    showHighscores();
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
            var score = data.score
            saveScore(score)
        };

        if (data.messageType == "SAVE") {
            var gameState = JSON.stringify(data.gameState);
            saveStates(gameState)
        };

        if (data.messageType == "LOAD_REQUEST") {
            loadStates();
        };
    });
});

