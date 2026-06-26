from django.db import models

class SurveyResponse(models.Model):
    """
    Creates database for storing thesis survey responses
    """
    
    image_id = models.IntegerField(null=True, blank=True) # File name of the image generated as the chatbot's avatar
    human_likeness = models.IntegerField(null=True, blank=True) # Human likeness rating of the chatbot's avatar
    
    age = models.IntegerField(null=True, blank=True) # Participant age

    # Participant gender based on gender options
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('non-binary', 'Non-binary'),
        ('prefer-not-to-say', 'Prefer not to say'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
    
    # Participant ratings (1-5) given for the 20 rating questions
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
    rq_11 = models.IntegerField(null=True, blank=True, choices=RATING_CHOICES)
    rq_12 = models.IntegerField(null=True, blank=True, choices=RATING_CHOICES)
    rq_13 = models.IntegerField(null=True, blank=True, choices=RATING_CHOICES)
    rq_14 = models.IntegerField(null=True, blank=True, choices=RATING_CHOICES)
    rq_15 = models.IntegerField(null=True, blank=True, choices=RATING_CHOICES)
    rq_16 = models.IntegerField(null=True, blank=True, choices=RATING_CHOICES)
    rq_17 = models.IntegerField(null=True, blank=True, choices=RATING_CHOICES)
    rq_18 = models.IntegerField(null=True, blank=True, choices=RATING_CHOICES)
    rq_19 = models.IntegerField(null=True, blank=True, choices=RATING_CHOICES)
    rq_20 = models.IntegerField(null=True, blank=True, choices=RATING_CHOICES)
    
    # Participant message content of the 5 open-ended questions
    opq_1 = models.TextField(null=True, blank=True)  
    opq_2 = models.TextField(null=True, blank=True) 
    opq_3 = models.TextField(null=True, blank=True) 
    opq_4 = models.TextField(null=True, blank=True)
    opq_5 = models.TextField(null=True, blank=True)  
    
    created_at = models.DateTimeField(auto_now_add=True) # Time survey is submitted
    
    class Meta:
        verbose_name = 'Survey Response'
        verbose_name_plural = 'Survey Responses'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Survey Response - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

# Uncomment for pretesting feedback
""""
class FeedbackResponse(models.Model):
    #Creates database for storing thesis survey responses
    
    # Participant response for 9 feedback questions
    f_1 = models.TextField(null=True, blank=True) 
    f_2 = models.TextField(null=True, blank=True) 
    f_3 = models.TextField(null=True, blank=True) 
    f_4 = models.TextField(null=True, blank=True) 
    f_5 = models.TextField(null=True, blank=True) 
    f_6 = models.TextField(null=True, blank=True) 
    f_7 = models.TextField(null=True, blank=True) 
    f_8 = models.TextField(null=True, blank=True) 
    f_9 = models.TextField(null=True, blank=True) 
    
    created_at = models.DateTimeField(auto_now_add=True) # Time feedback is sbumitted
    
    class Meta:
        verbose_name = 'Feedback Response'
        verbose_name_plural = 'Feedback Responses'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Feedback Response - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

"""