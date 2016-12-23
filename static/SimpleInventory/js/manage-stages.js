/* global Handlebars componentHandler url_api_v1_stage_list
   url_api_v1_stage_archive url_api_v1_stage_unarchive
   url_api_v1_stage_move_left url_api_v1_stage_move_right */
/* exported bubbleDown bubbleUp archiveStage unarchiveStage */

/* Global board state */
var stages_data;

/* Template for Handlebars to execute */
var source = $('#handlebars-stages').html();

$(document).ready(function(){
  /* Start templating */
  getstage_data();
});

/* Call APIs to get the JSON stage_data */
function getstage_data() {
  /* Get the list of stages */
  $.getJSON(url_api_v1_stage_list, function(stages){
    stages_data = {stages: []};
    for (var i = 0, len = stages.length; i < len; i++) {
      stages_data.stages[stages[i].fields.index] = {
        name: stages[i].fields.name,
        id: stages[i].pk,
        archived: stages[i].fields.archived,
      };
    }
    renderTemplate(stages_data);
  });
}

/* render compiled handlebars template */
function renderTemplate(stages_data){
  var template = Handlebars.compile(source);
  $('#stagesCard').html(template(stages_data));
  /* Make MDL re-register progress-bars and the like */
  componentHandler.upgradeDom();
}

/* Bubble a board up */
function bubbleUp(id) {
  $.getJSON(url_api_v1_stage_move_left.replace(0,id), function() {
    var stage_index = stages_data.stages.findIndex(function(element){
      return element.id == id;
    });
    var otherStage = stages_data.stages[stage_index-1];
    stages_data.stages[stage_index-1] = stages_data.stages[stage_index];
    stages_data.stages[stage_index] = otherStage;
    renderTemplate(stages_data);
  });
}

/* Bubble a board down */
function bubbleDown(id) {
  $.getJSON(url_api_v1_stage_move_right.replace(0,id), function() {
    var stage_index = stages_data.stages.findIndex(function(element){
      return element.id == id;
    });
    var otherStage = stages_data.stages[stage_index+1];
    stages_data.stages[stage_index+1] = stages_data.stages[stage_index];
    stages_data.stages[stage_index] = otherStage;
    renderTemplate(stages_data);
  });
}

/* Unarchive a stage */
function unarchiveStage(id) {
  $.getJSON(url_api_v1_stage_unarchive.replace(0, id), function() {
    var stage_index = stages_data.stages.findIndex(function(element){
      return element.id == id;
    });
    stages_data.stages[stage_index].archived = false;
    renderTemplate(stages_data);
  });
}

/* Archive a stage */
function archiveStage(id) {
  $.getJSON(url_api_v1_stage_archive.replace(0, id), function() {
    var stage_index = stages_data.stages.findIndex(function(element){
      return element.id == id;
    });
    stages_data.stages[stage_index].archived = true;
    renderTemplate(stages_data);
  });
}

$('#newStageForm').on('submit', addItem);
function addItem(event) {
  event.preventDefault();
  var form_data = $('#newStageForm');
  $.post(event.target.action, form_data.serialize(), function(response) {
    var stage = {};
    response = response[0];
    stage.id = response.pk;
    stage.name = response.fields.name;
    stage.archived = response.fields.archived;
    stages_data.stages[response.fields.index] = stage;
    renderTemplate(stages_data);
  }, 'json');
}
