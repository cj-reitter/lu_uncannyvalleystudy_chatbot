from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from numpy import random as rd
from ollama import Client
import json
import os

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
@require_http_methods(["GET"])
def get_random_profile_pic(request):
    """Return a random image from the media folder."""
    try:
        media_path = settings.MEDIA_ROOT
        if not os.path.exists(media_path):
            return JsonResponse({'error': 'Media folder not found'}, status=404)
        
        # Get all image files
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        images = [f for f in os.listdir(media_path) 
                  if os.path.isfile(os.path.join(media_path, f)) 
                  and os.path.splitext(f)[1].lower() in image_extensions]
        
        if not images:
            return JsonResponse({'error': 'No images found'}, status=404)
        
        random_image = rd.choice(images)
        image_url = f'{settings.MEDIA_URL}{random_image}'
        
        return JsonResponse({'image_url': image_url})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

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
    #chatbot_templates = ['chatbot_1.html', 'chatbot_2.html', 'chatbot_3.html']
    chatbot_templates = ['chatbot_1.html']
    ran_chatbot_template = rd.choice(chatbot_templates)

    return render(request, ran_chatbot_template)