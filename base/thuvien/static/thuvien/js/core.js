function laySachTheoMa(maSach) {
    return fetch('/api/sach/' + maSach)
        .then(response => response.json())
        .then(data => data);
}

function getCookieByName(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}