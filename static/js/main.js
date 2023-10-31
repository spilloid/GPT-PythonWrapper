document.addEventListener('DOMContentLoaded', (event) => {
	document.getElementById('send-button').addEventListener('click', sendMessage);
});

// Function to send the message to the Flask back-end
function sendMessage() {
	let message = document.getElementById('message-input').value;
	let messageBox = document.getElementById('message-input');
	let sendButton = document.getElementById('send-button');
	let loadingIcon = document.getElementById('loading-icon');

	// Disable the button and show a loading spinner (if you've styled one)
	messageBox.disabled = true;
	sendButton.disabled = true;
	sendButton.classList.add('loading');
	loadingIcon.hidden = false;

	fetch('/send_message', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ 'message': message })
	})
		.then(response => response.json())
		.then(data => {
			// Add new messages to the chat box
			let chatBox = document.getElementById('chat-box');
			chatBox.innerHTML += `<p>User: ${message}</p>`;
			chatBox.innerHTML += `<p>Assistant: ${data.message}</p>`;
			// Reset the input box
			document.getElementById('message-input').value = '';
			sendButton.disabled = false;
			sendButton.classList.remove('loading');
			loadingIcon.hidden = true;
			messageBox.disabled = false;
		})
		.catch((error) => {
			console.error('Error:', error);
			sendButton.disabled = false;
			messageBox.disabled = false;
			sendButton.classList.remove('loading');
			loadingIcon.hidden = true;
		});
}

document.getElementById('message-input').addEventListener('keypress', function(event) {
	if (event.keyCode === 13) {
		event.preventDefault(); // Prevent default Enter behavior (like submitting a form)
		sendMessage(); // Trigger the sendMessage function
	}
});
