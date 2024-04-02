// script.js
document.getElementById('evaluation-form').addEventListener('submit', function(e) {
    e.preventDefault();

    var input = document.getElementById('input').value;
    var output = document.getElementById('output').value;
    var apiKey = document.getElementById('api_key').value;
    var text = document.getElementById('text').value;

    fetch('/evaluate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            input: input.split('\n'),
            output: output.split('\n'),
            api_key: apiKey,
            text: text,
        }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').textContent = JSON.stringify(data, null, 2);
    });
});
