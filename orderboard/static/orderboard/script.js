function moveItem(id, direction) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            if (this.status == 200) {
                document.getElementById('stage_' + this.responseText).appendChild(
                    document.getElementById('card_' + id)
                );

            } else {
                alert('There was a problem moving that card.')
            }
        }

    };
    xhttp.open('GET', '/order/move/' + id + '/' + direction, true);
    xhttp.send();
}

function deleteItem(id) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            if (this.status == 200) {
                var element = document.getElementById('card_' + id)
                element.parentNode.removeChild(element);
            } else {
                alert('There was a problem removing that card.')
            }
        }
    };
    xhttp.open('GET', '/order/move/' + id + '/archive', true);
    xhttp.send();
}
