from django.contrib import admin
from .models import Post, Job, UserProfile
# Register your models here.
admin.site.register(Post) #追加

admin.site.register(Job) #追加
admin.site.register(UserProfile) #追加