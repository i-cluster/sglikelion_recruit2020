from  __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
#from django.db.models.signals import post_save
#from django.dispatch import receiver

# Create your models here.

class Application(models.Model):
    created_by = models.ForeignKey(User, verbose_name='지원자 이름', on_delete=models.CASCADE , blank=True, null=True)
    q1 = models.TextField(verbose_name='질문1', blank=True, null=True)
    q2 = models.TextField(verbose_name='질문2', blank=True, null=True)
    q3 = models.TextField(verbose_name='질문3', blank=True, null=True)
    q4 = models.TextField(verbose_name='질문4', blank=True, null=True)
    q5 = models.FileField(upload_to='user', verbose_name='첨부파일', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name='제출 날짜')
    final = models.BooleanField(default=False)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)#유저모델 onetoone
    phone = models.CharField(max_length=20, blank=True, verbose_name='연락처')
    major = models.CharField(max_length=255, verbose_name= '전공', null=True, blank=True)
    semester = models.IntegerField(verbose_name='누적학기', default=1)
    CLASSIFED_CHOICE_SET = (
        ('WED', '25(수)'),
        ('THUR', '26(목)'),
        ('FRI', '27(금)'),
    )
    interview_date = models.CharField(
        max_length=20,
        choices=CLASSIFED_CHOICE_SET,
        default='1',
        verbose_name='희망 면접 날짜'
    )

#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
 #   if created:
  #      Profile.objects.create(user=instance)

#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
 #   instance.profile.save()