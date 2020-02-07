function domain() {
    var url = window.location.href;
    var arr = url.split("/");
    var result = arr[0] + "//" + arr[2];
    return result;
}

// From https://docs.djangoproject.com/en/3.0/ref/csrf/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// var csrftoken = getCookie('csrftoken');

function saveStates(gameState) {
    console.log(domain())
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
            console.log("saved");
        }
    });
}

function loadStates() {
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
                $('#actions').empty();
                $('#actions').append("Loaded gamestate");
                console.log("loaded");
            }
            else {
                $('#actions').empty();
                $('#actions').append("No gamestate saved - could not load");
                console.log("loading no success");
            }
        }
    });
}

function saveScore(score){
    var destination = domain() + "/webshop/savescore/"; 
    var csrftoken = getCookie('csrftoken'); 
    $.ajax({
      url : destination,
      type : "POST",
      data : {
        gameID : gameID,
        score : score,
        csrfmiddlewaretoken: csrftoken
    },
       success : function(json) {
           console.log("highscore saved")
     }
   });
  }

function showHighscores() {
    var destination = domain() + "/webshop/highscore/";
    $.ajax ({
        url: destination,
        type : "GET",
        data: { gameID: gameID
    },
        success: function(json) {
        top10data = JSON.parse(json)
        $.each(top10data, function() {
            var user = this.fields.user;
            var score = this.fields.score;
            var listItem = '\n\t<li>' + user + ": " + score + '</li>';
            console.log(listItem);
            $('#highscores').prepend(listItem);
        });
        }
    });
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
            $('#score').empty();
            $('#score').append(data.score);
        };

        if (data.messageType == "SAVE") {
            var gameState = JSON.stringify(data.gameState);
            console.log(gameState)
            saveStates(gameState)
            $('#actions').empty();
            $('#actions').append("Saved gamestate");
        };

        if (data.messageType == "LOAD_REQUEST") {
            /*if (NO SAVED GAMESTATE) {
              $('#actions').empty();
              $('#actions').append("No game state saved - could not load");
            }
            else {*/
            loadStates();
            //}
        };
    });
});

