function showFile(e) {
    var files = e.target.files;
    for (var i = 0, f; f = files[i]; i++) {
        if (!f.type.match('image.*')) continue;
        var fr = new FileReader();
        fr.onload = (function (theFile) {
            return function (e) {
                var div = document.createElement("div");
                div.innerHTML = "<img style='max-width: 100%; border-radius: 5px;' src='" + e.target.result + "' />";
                div.classList.add('col')
                document.getElementById("list").insertBefore(div, null);
            };
        })(f);
        fr.readAsDataURL(f);
    }
}

document.getElementById('files').addEventListener('change', showFile, false);