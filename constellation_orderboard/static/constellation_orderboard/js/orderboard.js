/* global Handlebars componentHandler board_id url_api_v1_stage_list
url_api_v1_board_active_cards url_api_v1_card_move_left
url_api_v1_card_move_right url_api_v1_card_archive stage_form_id
stage_board_id dialogPolyfill */
/* exported moveItem deleteItem restoreItem addItem */

var dialog = document.querySelector('#newItem');
var message = document.querySelector('#message-toast');

/* Global board state */
var board_data;

/* Reverse look-ups for cards */
var stage_map, card_map;

/* Template for Handlebars to execute */
var source = $('#handlebars-board').html();

$(document).ready(function(){

  /* Register the dialog polyfill for most browsers */
  if (typeof(dialogPolyfill) != 'undefined') {
    dialogPolyfill.registerDialog(dialog);
  }

  /* Set the hidden board id in the form */
  $('#' + stage_board_id).val(board_id);

  /* Start templating */
  getboard_data();
});

/* Call APIs to get the JSON board_data */
function getboard_data() {
  /* Get the list of stages */
  board_data = {mdl_width: 12, stages: []};
  $.getJSON(url_api_v1_stage_list, function(stages){
    /* Sort stages by their index field */
    stages.sort(function(a, b) {
      return a.fields.index - b.fields.index;
    });
    /* Easily access stage and card locations by ID */
    stage_map = new Map();
    card_map = new Map();

    /* Put unarchived stages on the board */
    for (var i = 0, len = stages.length; i < len; i++) {
      if (!stages[i].fields.archived) {
        var array_length = board_data.stages.push({
          name: stages[i].fields.name,
          id: stages[i].pk,
          cards: [],
        });
        /* Map location to primary key */
        stage_map.set(stages[i].pk, array_length - 1);
      }
    }
    /* Set the invisible stage field in the new-card form to the first id */
    $('#' + stage_form_id).val(board_data.stages[0].id);

    /* Get cards and assign them to their stages */
    $.getJSON(url_api_v1_board_active_cards, function(cards){
      for (var i = 0, len = cards.length; i < len; i++) {
        var stage_index = stage_map.get(cards[i].fields.stage);
        board_data.stages[stage_index].cards.push({
          name: cards[i].fields.name,
          id: cards[i].pk,
          notes: cards[i].fields.notes,
          quantity: cards[i].fields.quantity,
          units: cards[i].fields.units,
        });
        /* Set card's stage for easy look-up */
        card_map.set(cards[i].pk, stage_index);
      }
      renderTemplate(board_data);
    })
      .fail(function(jqXHR) {
        if (jqXHR.status == 404) {
          message.MaterialSnackbar.showSnackbar({message: jqXHR.responseText});
        } else {
          message.MaterialSnackbar.showSnackbar({message: 'An error occured.'});
        }
        renderTemplate(board_data);
      });
  })
    .fail(function(jqXHR) {
      $('#showNewItem').hide();
      if (jqXHR.status == 404) {
        message.MaterialSnackbar.showSnackbar({message: jqXHR.responseText});
      } else {
        message.MaterialSnackbar.showSnackbar({message: 'An error occured.'});
      }
      renderTemplate(board_data);
    });
}

/* render compiled handlebars template */
function renderTemplate(board_data){
  board_data.mdl_width = Math.floor(12 / board_data.stages.length);
  var template = Handlebars.compile(source);
  $('#board').html(template(board_data));
  /* Make MDL re-register progress-bars and the like */
  componentHandler.upgradeDom();
}

/* Move a card left or right */
function moveItem(id, direction) {
  $('#card_' + id + '_progress').show();

  var url;
  if (direction == 'left') {
    url = url_api_v1_card_move_left.replace(0, id);
  } else if (direction == 'right') {
    url = url_api_v1_card_move_right.replace(0, id);
  }

  $.getJSON(url, function(action){
    var index = stage_map.get(action.stageID);
    var card_stage = card_map.get(id);
    var card_index = board_data.stages[card_stage].cards.findIndex(
      function(element){
        return element.id == id;
      });
    var card = board_data.stages[card_stage].cards[card_index];
    board_data.stages[index].cards.push(card);
    board_data.stages[card_stage].cards.splice(card_index, 1);
    card_map.set(id, index);
    renderTemplate(board_data);
  })
    .fail(function(jqXHR) {
      if (jqXHR.status == 500) {
        message.MaterialSnackbar.showSnackbar({message: jqXHR.responseText});
      } else {
        message.MaterialSnackbar.showSnackbar({message: 'An error occured.'});
      }
    });
}

/* Remove a card from the board */
function deleteItem(id) {
  $('#card_' + id + '_progress').show();
  $.get(url_api_v1_card_archive.replace(0, id), function(){
    var card_stage = card_map.get(id);
    var card_index = board_data.stages[card_stage].cards.findIndex(function(element){
      return element.id == id;
    });
    board_data.stages[card_stage].cards.splice(card_index, 1);
    card_map.delete(id);
    $('#card_' + id).effect('scale', {percent: 0}, 100, function(){
      renderTemplate(board_data);
    });
  })
    .fail(function(jqXHR) {
      if (jqXHR.status == 500) {
        message.MaterialSnackbar.showSnackbar({message: jqXHR.responseText});
      } else {
        message.MaterialSnackbar.showSnackbar({message: 'An error occured.'});
      }
    });
}

$('#newItemForm').on('submit', addItem);
function addItem(event) {
  event.preventDefault();
  dialog.close();
  var form_data = $('#newItemForm');
  $.post(event.target.action, form_data.serialize(), function(response) {
    var card = {};
    response = response[0];
    card.id = response.pk;
    card.name = response.fields.name;
    card.notes = response.fields.notes;
    card.quantity = response.fields.quantity;
    card.units = response.fields.units;
    board_data.stages[0].cards.push(card);
    card_map.set(response.pk, 0);
    renderTemplate(board_data);
  }, 'json')
    .fail(function(jqXHR) {
      if (jqXHR.status == 500 || jqXHR.status == 400) {
        message.MaterialSnackbar.showSnackbar({message: jqXHR.responseText});
      } else {
        message.MaterialSnackbar.showSnackbar({message: 'An error occured.'});
      }
    })
    .always(function() {
      form_data.trigger('reset');
    });
}

$('#showNewItem').click(openDialog);
function openDialog() {
  dialog.style.opacity = 0;
  dialog.style.transition = 'all 250ms ease';
  dialog.showModal();
  dialog.style.opacity = 1;
}

document.body.addEventListener('keydown', function(e) {
  if (e.keyCode == 27)
    dialog.close();
});

function clickedInDialog(mouseEvent) {
  var rect = dialog.getBoundingClientRect();
  return rect.top <= mouseEvent.clientY && mouseEvent.clientY <= rect.top + rect.height
    && rect.left <= mouseEvent.clientX && mouseEvent.clientX <= rect.left + rect.width;
}

$('body').on('click', 'dialog', function(e) {
  if($('dialog:visible').length && !clickedInDialog(e)) {
    dialog.close();
  }
});
