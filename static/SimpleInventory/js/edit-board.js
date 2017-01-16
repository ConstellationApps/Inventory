var message = document.querySelector('#message-toast');

$('#editBoardForm').on('submit', redirect);
function redirect(event) {
  event.preventDefault();
  var form_data = $('#editBoardForm');
    $.post(event.target.action, form_data.serialize(), function(response) {
	window.location.assign("/view/list");
  }, 'json')
    .fail(function(jqXHR) {
      if (jqXHR.status == 400 || jqXHR.status == 500) {
        message.MaterialSnackbar.showSnackbar({message: jqXHR.responseText});
      } else {
        message.MaterialSnackbar.showSnackbar({message: jqXHR.responseText});
      }
    });
}
