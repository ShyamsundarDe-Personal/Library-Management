from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    price = models.IntegerField()
    
    def __str__(self):
        return self.title
        
        
class Reader(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    
    def __str__(self):
        return self.username