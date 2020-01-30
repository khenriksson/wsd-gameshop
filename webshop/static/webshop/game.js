function getDomain(){
  var url = window.location.href;
  var arr = url.split("/");
  var result = arr[0] + "//" + arr[2];
  return result;
}

function saveStates(gameInfo){

  var destination = getDomain() + "/webshop/savegame/";
  $.ajax({
    url : destination,
    type : "GET",
    data : { game : game,
    user : user,
    gameInfo : gameInfo
  },
     success : function(json) {
     console.log("saved");
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

      //var gameState = {};
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
        //$('#actions').append(gameState);
      };
      if (data.messageType == "LOAD_REQUEST") {
        /*if (NO SAVED GAMESTATE) {
          $('#actions').empty();
          $('#actions').append("No game state saved - could not load");
        }
        else {*/
        // NOTE dummy data for testing load
        var gameState = {
          "playerItems": ['stone'],
          "score": 50.0
        };
        var message = {
          messageType: "LOAD", gameState
        };
        var frame = document.getElementById('gameframe');
        frame.contentWindow.postMessage(message, "*");
        $('#actions').empty();
        $('#actions').append("Loaded");
        //}
      };
    });
  });

