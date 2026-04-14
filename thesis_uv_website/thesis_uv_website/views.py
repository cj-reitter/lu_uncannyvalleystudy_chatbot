from django.shortcuts import render
from numpy import random as rd

def homepage(request):
    return render(request, 'home.html')

def chatbot(request):
    #chatbot_templates = ['chatbot_1.html', 'chatbot_2.html', 'chatbot_3.html']
    chatbot_templates = ['chatbot_1.html']
    ran_chatbot_template = rd.choice(chatbot_templates)

    return render(request, ran_chatbot_template)