class Chatbot {

    constructor() {
        this.args = {
            chatInterface: document.querySelector('.chat_interface'),
            messagesContainer: document.querySelector('.chat_interface_messages'),
            inputField: document.querySelector('.chat_interface_footer input'),
            sendButton: document.querySelector('.chat_interface_send_button')
        }

        this.messages = [];
    }

    display() {
        const {inputField, sendButton} = this.args;

        const greeting = 'Hello, how are you today?';
        this.addMessageToUI('assistant', greeting);
        this.messages.push({role: 'assistant', content: greeting});
        this.loadProfilePic();

        setTimeout(() => {
            window.location.href = '/survey';
        }, 300000);

        if (sendButton) {
            sendButton.addEventListener('click', () => this.onSendButton());
        }

        if (inputField) {
            inputField.addEventListener('keyup', ({key}) => {
                if (key === 'Enter') {
                    this.onSendButton();
                }
            });
        }
    }

    loadProfilePic() {
        const profileContainer = document.getElementById('profilepic');
        if (profileContainer) {
            profileContainer.innerHTML = '';
            const img = document.createElement('img');
            img.src = `/media/${CHATBOT_IMAGE_ID}.jpg`;
            img.alt = 'Chatbot Profile';
            profileContainer.appendChild(img);
        }
    }

    async onSendButton() {
        const {inputField, messagesContainer} = this.args;
        const userMessage = inputField.value.trim();
        
        if (userMessage === '') {
            return;
        }

        this.addMessageToUI('user', userMessage);
        inputField.value = '';

        const history = [...this.messages];
        this.messages.push({role: 'user', content: userMessage});

        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'messages_item messages_item--loading';
        loadingDiv.textContent = 'Generating...';
        loadingDiv.id = 'loading-indicator';
        messagesContainer.appendChild(loadingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        try {
            const response = await fetch('/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({message: userMessage, history: history})
            });

            if (!response.ok) {
                throw new Error('Chat request failed');
            }

            const data = await response.json();
            const botMessage = data.response;
            
            const loadingIndicator = document.getElementById('loading-indicator');
            if (loadingIndicator) {
                loadingIndicator.remove();
            }
            
            this.addMessageToUI('assistant', botMessage);
            this.messages.push({role: 'assistant', content: botMessage});
            
        } catch (error) {
            console.error('Error:', error);
            
            const loadingIndicator = document.getElementById('loading-indicator');
            if (loadingIndicator) {
                loadingIndicator.remove();
            }
            
            this.addMessageToUI('assistant', 'Sorry, there was an error processing your message.');
        }
    }

    addMessageToUI(role, content) {
        const {messagesContainer} = this.args;
        const messageDiv = document.createElement('div');
        const messageClass = role === 'assistant' ? 'messages_item--bot' : 'messages_item--user';
        messageDiv.className = `messages_item ${messageClass}`;
        messageDiv.textContent = content;
        messagesContainer.appendChild(messageDiv);
        
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

const chatbot = new Chatbot();
chatbot.display();