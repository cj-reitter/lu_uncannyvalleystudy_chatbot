class Chatbot {
    /**
     * Chatbot class that handles js for the chatbot webpage, including displaying message content to the
     *  UI and handling chatbot prompts when user clicks send
     */

    constructor() {
        /**
         * Fetches chatbot body, message list, input box, and send button from the site
         */

        this.args = {
            chatInterface: document.querySelector('.chat_interface'),
            messagesContainer: document.querySelector('.chat_interface_messages'),
            inputField: document.querySelector('.chat_interface_footer input'),
            sendButton: document.querySelector('.chat_interface_send_button')
        }

        this.messages = [];
    }

    display() {
        /**
         * Starts message list with chatbot greeting, and tracks time spent on page and if user message
         *  is sent
         */
        
        const {inputField, sendButton} = this.args;

        // Adds chatbot greeting to the top of the message list
        const greeting = 'Hello, how are you today?';
        this.addMessageToUI('assistant', greeting);
        this.messages.push({role: 'assistant', content: greeting});

        // Redirects to 'survey' webpage after 5 minutes have been spent on the page
        setTimeout(() => {
            window.location.href = '/survey';
        }, 300000);

        // Sends user message to chatbot if send button or "Enter" key clicked 
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

    async onSendButton() {
        /**
        * Retrieves user message whenever send button is clicked, adding it to the UI and sending it as a prompt
        *   to the chatbot.
        */

        // Retrieves user's message content from input field
        const {inputField, messagesContainer} = this.args;
        const userMessage = inputField.value.trim();
        
        // Prevents user from sending empty message
        if (userMessage === '') {
            return;
        }

        // Adds message content to the user side of the message display
        this.addMessageToUI('user', userMessage);
        inputField.value = '';

        // Adds user message to chatbot history 
        const history = [...this.messages];
        this.messages.push({role: 'user', content: userMessage});

        // Temporarily displays "Generating..." on chatbot side of message list while the chatbot generates
        // a response
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'messages_item messages_item--loading';
        loadingDiv.textContent = 'Generating...';
        loadingDiv.id = 'loading-indicator';
        messagesContainer.appendChild(loadingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        try {
            // Sends user message to Ollama api to generate chatbot message
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

            // Retrieves chatbot response and message content when recieved
            const data = await response.json();
            const botMessage = data.response;
            
            // Removes temporary "Generating..." message
            const loadingIndicator = document.getElementById('loading-indicator');
            if (loadingIndicator) {
                loadingIndicator.remove();
            }

            // Adds chatbot message content to the chatbot side of the message display 
            this.addMessageToUI('assistant', botMessage);
            this.messages.push({role: 'assistant', content: botMessage});
            
        } catch (error) {
            // Removes temporary "Generating..." message and adds error message if console logs an error
            console.error('Error:', error);
            
            const loadingIndicator = document.getElementById('loading-indicator');
            if (loadingIndicator) {
                loadingIndicator.remove();
            }
            
            this.addMessageToUI('assistant', 'Sorry, there was an error processing your message.');
        }
    }

    addMessageToUI(role, content) {
        /**
        * Adds content of message to the UI, either as a "--bot" message item or "--user" message item depending
        * on the role assigned to the message
        * @param {string} role Either 'user' or 'assitant', represents if its a participant/chatbot message
        *   respectively.
        * @param {string} content Content of the participant/chatbot's message sent
        */

        // Appends message content to the bot/user section of the message display depending on the role of the message
        const {messagesContainer} = this.args;
        const messageDiv = document.createElement('div');
        const messageClass = role === 'assistant' ? 'messages_item--bot' : 'messages_item--user';
        messageDiv.className = `messages_item ${messageClass}`;
        messageDiv.textContent = content;
        messagesContainer.appendChild(messageDiv);
        
        // Sets the UI to display the bottom of the message list
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

// Creates and displays new chatbot message chain every time the page loads
const chatbot = new Chatbot();
chatbot.display();