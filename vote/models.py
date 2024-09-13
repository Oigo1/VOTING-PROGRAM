from django.db import models
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100) # CAPTAIN, DEPUTY, PREFECTS

    def __str__(self):
        return self.name
    
class Contestant(models.Model):
    name = models.CharField(max_length=100)
    seat = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='contestant_images/', blank=True, null=True)  # Add this field
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    

class Vote(models.Model):
    voter_id = models.CharField(max_length=8, unique=True)
    contestant = models.ForeignKey(Contestant, on_delete=models.CASCADE)
    vote_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.voter_id} voted for {self.contestant.name}'