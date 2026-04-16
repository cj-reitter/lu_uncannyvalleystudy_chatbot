from django.shortcuts import render
from django.http import JsonResponse
from .models import SurveyResponse, FeedbackResponse
import json

def thesis_survey(request):
    if request.method == 'GET':
        return render(request, 'survey.html')
    
    elif request.method == 'POST':
            try:
                data = json.loads(request.body)
                
                age = data.get('age')
                age = int(age) if age and age.strip() else None
                
                gender = data.get('gender')
                gender = gender if gender and gender.strip() else None
                
                rating_questions = {}
                for i in range(1, 11):
                    key = f'rq_{i}'
                    value = data.get(key)
                    rating_questions[key] = int(value) if value else None
                
                open_ended_questions = {}
                for i in range(1, 5):
                    key = f'opq_{i}'
                    value = data.get(key, '').strip() or None
                    open_ended_questions[key] = value
                
                """
                if not all(rating_questions.values()):
                    return JsonResponse({
                        'success': False,
                        'error': 'Please answer all rating questions.'
                    }, status=400)
                """
                
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


def thesis_feedback(request):
    if request.method == 'GET':
        return render(request, 'feedback.html')
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            feedback_responses = {}
            for i in range(1, 10):
                key = f'f_{i}'
                value = data.get(key, '').strip() or None
                feedback_responses[key] = value
            
            feedback_response = FeedbackResponse(
                f_1=feedback_responses['f_1'],
                f_2=feedback_responses['f_2'],
                f_3=feedback_responses['f_3'],
                f_4=feedback_responses['f_4'],
                f_5=feedback_responses['f_5'],
                f_6=feedback_responses['f_6'],
                f_7=feedback_responses['f_7'],
                f_8=feedback_responses['f_8'],
                f_9=feedback_responses['f_9']
            )
            feedback_response.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Feedback saved successfully.'
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