document.addEventListener('DOMContentLoaded', function() {

    let form = document.querySelector('form');
    let chatbox = document.getElementById('chatbox');

    if (chatbox.children.length > 0) { //weird white box
        chatbox.style.display = "block";
    }

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        let formData = new FormData(form);
        let questionText = formData.get('question');

        fetch('/chat', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {

            let userMessage = document.createElement('p');
            userMessage.innerHTML = `<b>You:</b> ${questionText}`;
            
            let botResponseHtml = marked.marked(data.answer);  //turn markdown to html
            console.log(botResponseHtml)

            let botMessage = document.createElement('div');
            botMessage.innerHTML = `<div class="prose max-w-none"> ${botResponseHtml}`;

            chatbox.appendChild(userMessage);
            chatbox.appendChild(botMessage);
        })
        .then(() => {
            // After appending the content, check if chatbox has content
            if (chatbox.children.length > 0) {
                chatbox.style.display = "block";
            }
        });
    });
});
