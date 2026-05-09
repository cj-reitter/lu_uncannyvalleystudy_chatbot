from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import numpy as np
from numpy import random as rd
from ollama import Client
import json

from thesis_survey.views import thesis_survey#, thesis_feedback

HUMAN_LIKENESS = {
    1: 8, 2: 10, 3: 8, 4: 8, 5: 8,
    6: 4, 7: 5, 8: 7, 9: 9, 10: 7,
    11: 8, 12: 9, 13: 7, 14: 9, 15: 8,
    16: 5, 17: 7, 18: 7, 19: 6, 20: 4,
    21: 1, 22: 1, 23: 1, 24: 1, 25: 1,
    26: 1, 27: 2, 28: 5, 29: 3, 30: 6,
    31: 1, 32: 3, 33: 4, 34: 1, 35: 2,
    36: 2, 37: 2, 38: 1, 39: 1, 40: 1,
    41: 1, 42: 4, 43: 9, 44: 8, 45: 1,
    46: 2, 47: 1, 48: 2, 49: 1, 50: 2,
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
    levels = list(HUMAN_LIKENESS.values())
    level_counts = {l: levels.count(l) for l in set(levels)}
    weights = np.array([1 / level_counts[l] for l in levels], dtype=float)
    weights /= weights.sum()
    image_id = int(rd.choice(list(HUMAN_LIKENESS.keys()), p=weights))
    request.session['chatbot_image_id'] = image_id
    request.session['chatbot_human_likeness'] = HUMAN_LIKENESS[image_id]
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