import { Ollama } from 'ollama'
import settings from django.conf 

const fs = require('fs/promises');
const path = require('path');


OLLAMA_API_KEY = settings.OLLAMA_API_KEY

const ollama = new Ollama({
    host: "https://ollama.com",
    headers: {Authorization: 'Bearer ' + OLLAMA_API_KEY},
});


class Chatbot {

    constructor() {
        this.args = {
            chatBox: document.querySelector('.chatbox'),
            sendButton: document.querySelector('.send_button')
        }

        this.state = false;
        this.messages = [];
    }

    display() {
        generate_profile_pic();
        
        const {chatBox, sendButton} = this.args;

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node  = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
    }

    async onSendButton(chatbot){
        var textField = chatbox.querySelector('input');
        let text1 = textField.value
        if (text1 === "") {
            return
        }

        let msg1 = { role: "user", content: text1}
        this.messages.push(msg1);
        const response = await ollama.chat({
            model: 'deepseek-v3.2:cloud',
            messages: chatbot.messages,
            stream: true,
        })
        .then(r => response.part)
        .then(r => {
            let msg2 = {role: 'assistant', content: r.message.content};
            this.messages.push(msg2);
            this.updateChatText(chatbot)
            textField.value = ''
        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbot)
            textField.value = ''
        });
    }

    updateChatText(chatbot){
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {
            if (item.role === 'assistant')
            {
                html += '<div class="messages_item messages_item--bot">' + item.content + '</div>'
            }
            else
            {
                html += '<div class="messages_item messages_item--user">' + item.content + '</div>'
            }
        });

        const chatMessage = chatbot.querySelector('.chatbot_messages');
        chatMessage.innerHTML = html;
    }

    generate_profile_pic() {
    const profilePicPath = path.join(__dirname, 'media');
    const files = fs.readdir(profilePicPath);

    const profileContainer = document.getElementById("profilepic")
    profileContainer.innerHTML = "";
    const img = document.createElement("img");
    img.src = `/static/media/${files[Math.floor(Math.random() * files.length)]}`;
    profileContainer.appendChild(img);
    }

}


const chatbot = new Chatbot();
chatbot.display();