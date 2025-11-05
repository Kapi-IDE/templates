const chatBox = document.getElementById('chatBox');

// Set focus to the text box when the page loads
window.onload = function() {
    document.querySelector('.text-box').focus();
};

// Handle sending messages when the user presses 'Enter'
document.querySelector('.text-box').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        const userInput = this.value.trim();
        if (userInput !== '') {
            // Display the user's message in the chat box
            chatBox.value += `You: ${userInput}\n`;
            this.value = '';

            // Scroll to the bottom of the textarea
            chatBox.scrollTop = chatBox.scrollHeight;

            // Send the user's message to the backend
            fetch('http://localhost:8000/customer-service/invoke', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'accept': 'application/json'
                },
                body: JSON.stringify({
                    input: userInput,
                    config: {},
                    kwargs: {}
                })
            })
            .then(response => response.json())
            .then(data => {
                const botMessage = data.output || 'Sorry, I did not understand that.';
                // Display the bot's response in the chat box
                chatBox.value += `Mitra: ${botMessage}\n`;

                // Scroll to the bottom of the textarea
                chatBox.scrollTop = chatBox.scrollHeight;

                // Play the audio response
                document.getElementById('audio-response').play();
            })
            .catch(error => {
                console.error('Error:', error);
                // Handle errors by displaying a message in the chat box
                chatBox.value += 'Mitra: Sorry, there was an error processing your request.\n';

                // Scroll to the bottom of the textarea
                chatBox.scrollTop = chatBox.scrollHeight;

                // Play the audio response
                document.getElementById('audio-response').play();
            });
        }
    }
});
