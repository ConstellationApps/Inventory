function moveItem(id) {
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById(this.responseText).appendChild(
                document.getElementById('card_' + id)
            );
        } else {
            alert("There was a problem moving that card.")
        }
    };
    xhttp.open("GET", "/order/move/" + id, true);
    xhttp.send();
}
