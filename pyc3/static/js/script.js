document.getElementById("api").addEventListener("click", function() {
    fetch('{{ url_for("give_api") }}')  // Utilizează url_for pentru a genera ruta corectă în Flask
        .then(response => response.json())
        .then(data => {
            document.getElementById("response").innerHTML = data.message;
        });
});

document.getElementById('error-log').addEventListener('click', () => {
    fetch('{{ url_for("errors") }}')
    .then(response => response.json())
    .then(data =>{
        console.log(data)
        const container = document.getElementById("log")
        container.innerHTML = ''

        data.forEach(entry => {
        const paragraph = document.createElement("p");
        paragraph.textContent = `Timestamp: ${entry.timestamp}, Error: ${entry.error_message}`;
        container.appendChild(paragraph);
    });

    } )
})