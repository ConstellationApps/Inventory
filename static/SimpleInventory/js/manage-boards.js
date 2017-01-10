/* global Handlebars componentHandler url_api_v1_board_list
   url_view_board url_api_v1_board_archive url_api_v1_board_unarchive */
/* exported archiveBoard unarchiveBoard */

/* Global board state */
var boards_data;

var message = document.querySelector('#message-toast');

/* Template for Handlebars to execute */
var source = $('#handlebars-board').html();

$(document).ready(function(){
  /* Start templating */
  getboard_data();
});

/* Call APIs to get the JSON board_data */
function getboard_data() {
  /* Get the list of stages */
  $.getJSON(url_api_v1_board_list, function(boards){
    boards_data = { active_boards: [], inactive_boards: [] };
    for (var i = 0, len = boards.length; i < len; i++) {
      var board_array;
      if(boards[i].fields.archived == false) {
        board_array = boards_data.active_boards;
      } else {
        board_array = boards_data.inactive_boards;
      }
      board_array.push({
        name: boards[i].fields.name,
        id: boards[i].pk,
        url: url_view_board.replace(0, boards[i].pk)
      });
    }
    renderTemplate(boards_data);
  })
    .fail(function(jqXHR) {
      if (jqXHR.status == 404) {
        message.MaterialSnackbar.showSnackbar({message: jqXHR.responseText});
      } else {
        message.MaterialSnackbar.showSnackbar({message: 'An error occured.'});
      }
    });
}

/* render compiled handlebars template */
function renderTemplate(boards_data){
  var template = Handlebars.compile(source);
  $('#boardsCard').html(template(boards_data));
  /* Make MDL re-register progress-bars and the like */
  componentHandler.upgradeDom();
}

/* archive a board */
function archiveBoard(id) {
  $.getJSON(url_api_v1_board_archive.replace(0, id), function(){
    var board_index = boards_data.active_boards.findIndex(function(element){
      return element.id == id;
    });
    boards_data.inactive_boards.push(boards_data.active_boards[board_index]);
    boards_data.active_boards.splice(board_index, 1);
    renderTemplate(boards_data);
  })
    .fail(function(jqXHR) {
      if (jqXHR.status == 500) {
        message.MaterialSnackbar.showSnackbar({message: jqXHR.responseText});
      } else {
        message.MaterialSnackbar.showSnackbar({message: 'An error occured.'});
      }
    });
}

/* unarchive a board */
function unarchiveBoard(id) {
  $.getJSON(url_api_v1_board_unarchive.replace(0, id), function(){
    var board_index = boards_data.inactive_boards.findIndex(function(element){
      return element.id == id;
    });
    boards_data.active_boards.push(boards_data.inactive_boards[board_index]);
    boards_data.inactive_boards.splice(board_index, 1);
    renderTemplate(boards_data);
  })
    .fail(function(jqXHR) {
      if (jqXHR.status == 500) {
        message.MaterialSnackbar.showSnackbar({message: jqXHR.responseText});
      } else {
        message.MaterialSnackbar.showSnackbar({message: 'An error occured.'});
      }
    });
}

$('#newBoardForm').on('submit', addItem);
function addItem(event) {
  event.preventDefault();
  var form_data = $('#newBoardForm');
  $.post(event.target.action, form_data.serialize(), function(response) {
    var board = {};
    response = response[0];
    board.id = response.pk;
    board.name = response.fields.name;
    board.url = url_view_board.replace(0, response.pk);
    boards_data.active_boards.push(board);
    renderTemplate(boards_data);
  }, 'json')
    .fail(function(jqXHR) {
      if (jqXHR.status == 400 || jqXHR.status == 500) {
        message.MaterialSnackbar.showSnackbar({message: jqXHR.responseText});
      } else {
        message.MaterialSnackbar.showSnackbar({message: 'An error occured.'});
      }
    });
}
