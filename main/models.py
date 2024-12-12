from django.db import models

# Create your models here.

class Article(models.Model):
    headline  = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    summary = models.TextField()
    date = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.title