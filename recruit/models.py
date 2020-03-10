from  __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
#from django.db.models.signals import post_save
#from django.dispatch import receiver

# Create your models here.

class Application(models.Model):
    objects = models.Manager()
    q1 = models.TextField(default="")
    q2 = models.TextField(default="")
    q3 = models.TextField(default="")
    q4 = models.TextField(default="")
    date = models.DateTimeField(default=timezone.now)
    final = models.BooleanField(default=False)
    author = models.CharField(max_length=30)

class Profile(models.Model):
    objects = models.Manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE)#유저모델 onetoone
    phone = models.CharField(max_length=20, blank=True)
    info = models.CharField(max_length=20, blank=True)
    
#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
 #   if created:
  #      Profile.objects.create(user=instance)

#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
 #   instance.profile.save()