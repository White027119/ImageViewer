from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    
class Plan(models.Model):
    title = models.CharField(max_length=100)
    max_height = models.IntegerField()
    create_link = models.BooleanField(default=False)
    exp_range = models.IntegerField()
    def __str__(self):
        return self.title
    
class ImageUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
    
class ExpLink(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    link = models.CharField(max_length=100)
    exp_date = models.IntegerField()
    def __str__(self):
        return self.link