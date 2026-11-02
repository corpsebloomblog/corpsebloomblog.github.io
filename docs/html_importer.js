const elements = document.getElementsByClassName("import");

fetch("index.html").then(Response => console.log(Response.text()));