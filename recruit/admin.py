from django.contrib import admin
from .models import Application, Profile

# Register your models here.
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    models = Application
    verbose_name = '지원서'
    verbose_name_plural = '지원서'

@admin.register(Profile)
class ApplicationAdmin(admin.ModelAdmin):
    models = Profile
    verbose_name = '지원자 프로필'
    verbose_name_plural = '지원자 프로필'