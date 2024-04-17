from django.db import models

class Tweet(models.Model):
    text = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)  
    date = models.DateTimeField(blank=True, null=True)  
    likes = models.IntegerField(default=0) 
    comments = models.IntegerField(default=0) 
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]  # Display first 50 characters of tweet text
