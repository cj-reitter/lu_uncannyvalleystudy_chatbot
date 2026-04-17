from django.db import models

class ImageRanking(models.Model):
    """Model to store image rankings for human likeness."""
    
    session_id = models.CharField(max_length=255, default='legacy')
    image_name = models.CharField(max_length=255)
    
    RANKING_CHOICES = [(i, f'{i}%') for i in range(10, 110, 10)]
    ranking = models.IntegerField(choices=RANKING_CHOICES)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Image Ranking'
        verbose_name_plural = 'Image Rankings'
        ordering = ['image_name']
        unique_together = ['session_id', 'image_name']
    
    def __str__(self):
        return f"[{self.session_id[:8]}] {self.image_name} - {self.ranking}%"
