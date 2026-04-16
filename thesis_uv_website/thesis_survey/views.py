from django.shortcuts import render
from django.http import JsonResponse
from .models import SurveyResponse
import json

def thesis_survey(request):
    if request.method == 'GET':
        return render(request, 'survey.html')
    
    elif request.method == 'POST':
            try:
                # Handle JSON POST request
                data = json.loads(request.body)
                
                # Convert empty strings to None for optional fields
                age = data.get('age')
                age = int(age) if age and age.strip() else None
                
                gender = data.get('gender')
                gender = gender if gender and gender.strip() else None
                
                # Rating questions (rq_1 through rq_10)
                rating_questions = {}
                for i in range(1, 11):
                    key = f'rq_{i}'
                    value = data.get(key)
                    rating_questions[key] = int(value) if value else None
                
                # Open-ended questions (opq_1 through opq_4)
                open_ended_questions = {}
                for i in range(1, 5):
                    key = f'opq_{i}'
                    value = data.get(key, '').strip() or None
                    open_ended_questions[key] = value
                
                # Validate that all rating questions are answered
                if not all(rating_questions.values()):
                    return JsonResponse({
                        'success': False,
                        'error': 'Please answer all rating questions.'
                    }, status=400)
                
                # Create and save the survey response
                survey_response = SurveyResponse(
                    age=age,
                    gender=gender,
                    rq_1=rating_questions['rq_1'],
                    rq_2=rating_questions['rq_2'],
                    rq_3=rating_questions['rq_3'],
                    rq_4=rating_questions['rq_4'],
                    rq_5=rating_questions['rq_5'],
                    rq_6=rating_questions['rq_6'],
                    rq_7=rating_questions['rq_7'],
                    rq_8=rating_questions['rq_8'],
                    rq_9=rating_questions['rq_9'],
                    rq_10=rating_questions['rq_10'],
                    opq_1=open_ended_questions['opq_1'],
                    opq_2=open_ended_questions['opq_2'],
                    opq_3=open_ended_questions['opq_3'],
                    opq_4=open_ended_questions['opq_4']
                )
                survey_response.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Survey response saved successfully.',
                    'redirect_url': '/completion/'  # Change this to your completion page URL
                })
            
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid JSON data.'
                }, status=400)
            except ValueError:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid data format.'
                }, status=400)
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=500)