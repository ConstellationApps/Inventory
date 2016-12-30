/* global Handlebars componentHandler url_api_v1_board_list url_view_board */

/* Global board state */
var boards_data;

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
    boards_data = { boards: [] };
    for (var i = 0, len = boards.length; i < len; i++) {
      if(boards[i].fields.archived == false) {
        boards_data.boards.push({
          name: boards[i].fields.name,
          desc: boards[i].fields.desc,
          id: boards[i].pk,
          url: url_view_board.replace(0, boards[i].pk)
        });
      }
    }
    renderTemplate(boards_data);
  });
}

/* render compiled handlebars template */
function renderTemplate(boards_data){
  var template = Handlebars.compile(source);
  $('#boardsCard').html(template(boards_data));
  /* Make MDL re-register progress-bars and the like */
  componentHandler.upgradeDom();
}
