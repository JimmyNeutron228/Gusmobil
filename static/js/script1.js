function showFile(e) {
    var files = e.target.files;
    for (var i = 0, f; f = files[i]; i++) {
        if (!f.type.match('image.*')) continue;
        var fr = new FileReader();
        fr.onload = (function (theFile) {
            return function (e) {
                var div = document.createElement("div");
                div.innerHTML = "<img src='" + e.target.result + "' />";
                document.getElementById("list").insertBefore(div, null);
            };
        })(f);
        fr.readAsDataURL(f);
    }
}

document.getElementById('files').addEventListener('change', showFile, false);