from django.db import models

class SurveyResponse(models.Model):
    
    age = models.IntegerField(null=True, blank=True)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('non-binary', 'Non-binary'),
        ('prefer-not-to-say', 'Prefer not to say'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
    
    
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    rq_1 = models.IntegerField(null=True, blank=True, choices=RATING_CHOICES)  
    rq_2 = models.IntegerField(null=True, blank=True, choices=RATING_CHOICES)  
    rq_3 = models.IntegerField(null=True, blank=True, choices=RATING_CHOICES)  
    rq_4 = models.IntegerField(null=True, blank=True, choices=RATING_CHOICES)  
    rq_5 = models.IntegerField(null=True, blank=True, choices=RATING_CHOICES)  
    rq_6 = models.IntegerField(null=True, blank=True, choices=RATING_CHOICES)  
    rq_7 = models.IntegerField(null=True, blank=True, choices=RATING_CHOICES)  
    rq_8 = models.IntegerField(null=True, blank=True, choices=RATING_CHOICES)  
    rq_9 = models.IntegerField(null=True, blank=True, choices=RATING_CHOICES) 
    rq_10 = models.IntegerField(null=True, blank=True, choices=RATING_CHOICES) 
    
    opq_1 = models.TextField(null=True, blank=True)  
    opq_2 = models.TextField(null=True, blank=True) 
    opq_3 = models.TextField(null=True, blank=True) 
    opq_4 = models.TextField(null=True, blank=True)  
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Survey Response'
        verbose_name_plural = 'Survey Responses'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Survey Response - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class FeedbackResponse(models.Model):
    """Model to store pre-testing feedback responses."""
    
    f_1 = models.TextField(null=True, blank=True) 
    f_2 = models.TextField(null=True, blank=True) 
    f_3 = models.TextField(null=True, blank=True) 
    f_4 = models.TextField(null=True, blank=True) 
    f_5 = models.TextField(null=True, blank=True) 
    f_6 = models.TextField(null=True, blank=True) 
    f_7 = models.TextField(null=True, blank=True) 
    f_8 = models.TextField(null=True, blank=True) 
    f_9 = models.TextField(null=True, blank=True) 
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Feedback Response'
        verbose_name_plural = 'Feedback Responses'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Feedback Response - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

