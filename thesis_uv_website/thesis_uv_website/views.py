from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from numpy import random as rd
from ollama import Client
import json

from thesis_survey.views import thesis_survey#, thesis_feedback

IMAGE_LIKENESS = {
    1: 1, 2: 1, 3: 1, 4: 1, 5: 1,
    6: 2, 7: 2, 8: 2, 9: 2, 10: 2,
    11: 3, 12: 3, 13: 3, 14: 3, 15: 3,
    16: 4, 17: 4, 18: 4, 19: 4, 20: 4,
    21: 5, 22: 5, 23: 5, 24: 5, 25: 5,
    26: 6, 27: 6, 28: 6, 29: 6, 30: 6,
    31: 7, 32: 7, 33: 7, 34: 7, 35: 7,
    36: 8, 37: 8, 38: 8, 39: 8, 40: 8,
    41: 9, 42: 9, 43: 9, 44: 9, 45: 9,
    46: 10, 47: 10, 48: 10, 49: 10, 50: 10,
}

# Home View

def homepage(request):
    return render(request, 'home.html')

# Chatbot View

def get_ollama_client():
    headers = {}
    if settings.OLLAMA_API_KEY:
        headers['Authorization'] = 'Bearer ' + settings.OLLAMA_API_KEY
    client = Client(
        host=settings.OLLAMA_HOST,
        headers=headers,
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
        history = data.get('history', [])

        if not user_message:
            return JsonResponse({'error': 'Empty message'}, status=400)

        client = get_ollama_client()

        messages = (
            [system_prompt, bot_greeting]
            + history
            + [{'role': 'user', 'content': user_message}]
        )
        
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
    image_id = rd.randint(1, 50)
    request.session['chatbot_image_id'] = image_id
    request.session['chatbot_human_likeness'] = IMAGE_LIKENESS[image_id]
    return render(request, 'chatbot_1.html', {'chatbot_image_id': image_id})

# Survey View
def survey(request):
    return thesis_survey(request)

# Uncomment for pretesting
""""
# Feedback View
def feedback(request):
    return thesis_feedback(request)
"""

# Endpage View
def endpage(request):
    return render(request, 'endpage.html')

# Ranking View
def ranking(request):
    return render(request, 'ranking.html')