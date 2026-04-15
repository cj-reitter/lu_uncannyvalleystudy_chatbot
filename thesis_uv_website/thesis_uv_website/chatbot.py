from ollama import Client
import os

client = Client(
    host = 'https://ollama.com',
    headers = {'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY')}
)

system_prompt = [
    {
        'role': 'system',
        'content': 'You are a friendly chatbot talking to a human user. Act like a friendly stranger. Keep answers brief, formatted like small talk, and keep the conversation flowing. Divert the conversation if it becomes too intimate.',
    }
]

messages = [
    {
        'role': 'assistant',
        'content': 'Hello! How are you?'
    }
]

for part in client.chat('deepseek-v3.2:cloud', messages = system_prompt + messages, stream = True):
    print(part.message.content, end = '', flush = True)