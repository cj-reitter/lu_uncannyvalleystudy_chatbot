from django.db import models

class ImageRanking(models.Model):
    """
    Creates database for storing ranking results
    """
    
    session_id = models.CharField(max_length=255, default='legacy') # User's CSRF token 
    image_name = models.CharField(max_length=255) # Image name being ranked
    
    RANKING_CHOICES = [(i, f'{i}%') for i in range(10, 110, 10)]
    ranking = models.IntegerField(choices=RANKING_CHOICES) # Ranking given to image (10-100%)
    
    created_at = models.DateTimeField(auto_now_add=True) # Time rank is submitted
    
    class Meta:
        verbose_name = 'Image Ranking'
        verbose_name_plural = 'Image Rankings'
        ordering = ['image_name']
        unique_together = ['session_id', 'image_name']
    
    def __str__(self):
        return f"[{self.session_id[:8]}] {self.image_name} - {self.ranking}%"
