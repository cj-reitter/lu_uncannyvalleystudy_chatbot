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

# Human likeness rating assigned to the 50 images in the avatar dataset
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

def homepage(request):
    """
    Loads 'home' webpage
    """
    return render(request, 'home.html')

def get_ollama_client():
    """
    Loads Ollama API client for chatbot responses
    """

    # Loads Ollama API key and host (local host by default in settings)
    headers = {}
    if settings.OLLAMA_API_KEY:
        headers['Authorization'] = 'Bearer ' + settings.OLLAMA_API_KEY
    client = Client(
        host=settings.OLLAMA_HOST,
        headers=headers,
    )
    return client

# System message for chatbot to follow throughout the conversation
system_prompt = {
    'role': 'system',
    'content': 'You are a friendly chatbot talking to a human user. Act like a friendly stranger. Keep answers brief, formatted like small talk, and keep the conversation flowing. Avoid asking for personal infromation from the user. Divert the conversation if it becomes too intimate.',
}

# Chatbot's initial message in the chatbot history
bot_greeting = {
    'role': 'assistant',
    'content': 'Hello, how are you today?'
}

@csrf_exempt
@require_http_methods(["POST"])
def chat_api(request):
    """
    Calls Ollama API for chatbot message generation when webpage securely calls the site
    """

    try:

        # Loads user message and chatbot history
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        history = data.get('history', [])

        # Throws error if user message somehow empty
        if not user_message:
            return JsonResponse({'error': 'Empty message'}, status=400)

        client = get_ollama_client() # Loads Ollama API client

        # Sets message history for the prompt, including the system prompt
        messages = (
            [system_prompt, bot_greeting]
            + history
            + [{'role': 'user', 'content': user_message}]
        )
        
        # Calls Deepseek v3.2 to generate a response based on the message history
        response = client.chat(
            model='deepseek-v3.2:cloud',
            messages=messages,
            stream=False
        )
        
        # Returns Deepseek's generated response as the chatbot's response
        bot_message = response['message']['content']
        return JsonResponse({'response': bot_message})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def chatbot(request):
    """
    Loads 'chatbot' page and random image for the chatbot avatar
    """

    # Sets weight list for image selection so each human likeness ranking (1-10) has a uniform chance of
    # being selected
    levels = list(HUMAN_LIKENESS.values())
    level_counts = {l: levels.count(l) for l in set(levels)}
    weights = np.array([1 / level_counts[l] for l in levels], dtype=float)
    weights /= weights.sum()

    # Randomly selects an image for the avatar dataset for the chatbot avatar weighted on human likeness values
    image_id = int(rd.choice(list(HUMAN_LIKENESS.keys()), p=weights))
    request.session['chatbot_image_id'] = image_id
    request.session['chatbot_human_likeness'] = HUMAN_LIKENESS[image_id]

    # Loads 'chatbot' webpage and the randomly selected image
    return render(request, 'chatbot_1.html', {'chatbot_image_id': image_id})

def survey(request):
    """
    Loads 'survey' webpage
    """
    return thesis_survey(request)

# Uncomment for pretesting
""""
# Feedback View
def feedback(request):

    Loads 'feedback' webpage

    return thesis_feedback(request)
"""

def endpage(request):
    """
    Load 'endpage' webpage
    """
    return render(request, 'endpage.html')

def ranking(request):
    """
    Loads 'ranking' webpage
    """
    return render(request, 'ranking.html')