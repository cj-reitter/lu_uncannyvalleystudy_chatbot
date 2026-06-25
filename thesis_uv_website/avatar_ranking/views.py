from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .models import ImageRanking
import json
import random

def ranking(request):
    """
    Directs website to "ranking" page.
    """
    return render(request, 'ranking.html')


def get_next_image(request):
    """
    Fetches a new unranked profile pciture
    """
    try:

        # Creates session id if no session id yet, otherwise stores user session id
        if not request.session.session_key:
            request.session.create()
        session_id = request.session.session_key

        # Goes through image list and matches user's session id with image name to obtain all unranked images.
        all_images = [f"{i}.jpg" for i in range(1, 51)]
        
        ranked_images = set(
            ImageRanking.objects.filter(session_id=session_id)
            .values_list('image_name', flat=True)
        )
        
        unranked_images = [img for img in all_images if img not in ranked_images]

        # If all images ranked, marks the ranking task as completed
        if not unranked_images:
            return JsonResponse({
                'success': True,
                'completed': True,
                'message': 'All images have been ranked!'
            })
        

        # Of the unranked images, randomly selects an image from the set
        selected_image = random.choice(unranked_images)
        image_url = f"{settings.MEDIA_URL}{selected_image}"
        

        # Returns the new random image and the ranking task progress (ranked images/50)
        return JsonResponse({
            'success': True,
            'completed': False,
            'image_name': selected_image,
            'image_url': image_url,
            'progress': {
                'ranked': len(ranked_images),
                'total': len(all_images)
            }
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def submit_ranking(request):
    """
    Stores user ranking whenever user submits a ranking.
    """
    if request.method == 'POST':
        try:

            # Creates session id if no session id yet, otherwise stores user session id
            if not request.session.session_key:
                request.session.create()
            session_id = request.session.session_key

            # Fetches image being ranked and the user rank of the image
            data = json.loads(request.body)
            
            image_name = data.get('image_name', '').strip()
            ranking_value = data.get('ranking')
            
            # Error if image loads incorrectly or no rank has been selected
            if not image_name or not ranking_value:
                return JsonResponse({
                    'success': False,
                    'error': 'Missing image name or ranking value.'
                }, status=400)
            
            # Error if ranking value somehow not 10-100
            ranking_value = int(ranking_value)
            if ranking_value not in range(10, 110, 10):
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid ranking value.'
                }, status=400)
            
            # Stores image ranking data and time rank was submitted to the image ranking database
            image_ranking, created = ImageRanking.objects.update_or_create(
                session_id=session_id,
                image_name=image_name,
                defaults={'ranking': ranking_value}
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Ranking saved successfully.'
            })
        
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON data.'
            }, status=400)
        except ValueError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid ranking value.'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method.'
    }, status=400)
