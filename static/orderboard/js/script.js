function moveItem(id, direction) {
  $('#card_' + id + '_progress').show();

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4) {
      if (this.status == 200) {
        $('#card_' + id).appendTo('#stage_' + this.responseText)
        $('#card_' + id + '_progress').hide();
      } else {
        alert('There was a problem moving that card.');
      }
    }

  };
  xhttp.open('GET', '/order/move/' + id + '/' + direction, true);
  xhttp.send();
}

function deleteItem(id) {
  $('#card_' + id + '_progress').show();
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4) {
      if (this.status == 200) {
        $('#card_' + id).effect("scale", {percent: 0}, 100, function(){
          $('#card_' + id).remove();
        } );
      } else {
        alert('There was a problem removing that card.');
      }
    }
  };
  xhttp.open('GET', '/order/move/' + id + '/archive', true);
  xhttp.send();
}

function restoreItem(id) {
  $('#card_' + id + '_progress').show();
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4) {
      if (this.status == 200) {
        $('#card_' + id).effect("scale", {percent: 0}, 100, function(){
          $('#card_' + id).parent().remove();
        } );
      } else {
        alert('There was a problem restoring that card.');
      }
    }
  };
  xhttp.open('GET', '/order/move/' + id + '/left', true);
  xhttp.send();
}

$(document).ready(function() {
  $('.modal-trigger').leanModal();
  $('.button-collapse').sideNav();
});
