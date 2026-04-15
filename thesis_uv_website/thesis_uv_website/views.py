from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from numpy import random as rd
from ollama import Client
import json

# Home View

def homepage(request):
    return render(request, 'home.html')

# Chatbot View

def get_ollama_client():
    client = Client(
    host='https://ollama.com',
    headers={'Authorization': 'Bearer ' + settings.OLLAMA_API_KEY}
    )
    
    return client

system_prompt = {
    'role': 'system',
    'content': 'You are a friendly chatbot talking to a human user. Act like a friendly stranger. Keep answers brief, formatted like small talk, and keep the conversation flowing. Avoid asking for personal infromation from the user. Divert the conversation if it becomes too intimate.',
}

bot_greeting = {
    'role': 'assistant',
    'content': 'Hello, how are you today?'
}

@csrf_exempt
@require_http_methods(["POST"])
def chat_api(request):
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({'error': 'Empty message'}, status=400)
        
        client = get_ollama_client()
        
        messages = [
            system_prompt,
            bot_greeting,
            {'role': 'user', 'content': user_message}
        ]
        
        response = client.chat(
            model='deepseek-v3.2:cloud',
            messages=messages,
            stream=False
        )
        
        bot_message = response['message']['content']
        return JsonResponse({'response': bot_message})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Chatbot View
def chatbot(request):
    chatbot_templates = ['chatbot_1.html', 'chatbot_2.html']
    ran_chatbot_template = rd.choice(chatbot_templates)

    return render(request, ran_chatbot_template)

# Survey View
def survey(request):
    return render(request, 'survey.html')