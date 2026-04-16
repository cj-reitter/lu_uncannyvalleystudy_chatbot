from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .models import ImageRanking
import json
import random

def ranking(request):
    """Main page for image ranking."""
    return render(request, 'ranking.html')


def get_next_image(request):
    """Get the next unranked image."""
    try:
        all_images = [f"{i}.jpg" for i in range(1, 51)]
        
        ranked_images = set(ImageRanking.objects.values_list('image_name', flat=True))
        
        unranked_images = [img for img in all_images if img not in ranked_images]
        
        if not unranked_images:
            return JsonResponse({
                'success': True,
                'completed': True,
                'message': 'All images have been ranked!'
            })
        
        selected_image = random.choice(unranked_images)
        image_url = f"{settings.MEDIA_URL}{selected_image}"
        
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
    """Submit a ranking for an image."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            image_name = data.get('image_name', '').strip()
            ranking_value = data.get('ranking')
            
            if not image_name or not ranking_value:
                return JsonResponse({
                    'success': False,
                    'error': 'Missing image name or ranking value.'
                }, status=400)
            
            ranking_value = int(ranking_value)
            if ranking_value not in range(10, 110, 10):
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid ranking value.'
                }, status=400)
            
            image_ranking, created = ImageRanking.objects.update_or_create(
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
