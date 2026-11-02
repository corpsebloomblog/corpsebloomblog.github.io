const elements = document.getElementsByClassName("import");

for (let i = 0; i < elements.length; i++) {
    const element = elements[i];
    const file = element.getAttribute("from");
    fetch("/"+file)
        .then(Response => Response.text())
        .then(data => element.innerHTML = data);
}
