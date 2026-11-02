const elements = document.getElementsByClassName("import");

for (let i = 0; i < elements.length; i++) {
    const element = elements[i];
    console.log(element.getAttribute("from"));
    // fetch().then(Response => console.log(Response.text()));
}
