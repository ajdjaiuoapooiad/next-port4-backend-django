# coding: utf-8
from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserProfileView
from . import views

urlpatterns = [
  path('device/', views.TaskCreateListAPIView.as_view()),
  path('device/<int:pk>/', views.TaskRetrieveUpdataDestroyAPIView.as_view()),
  path('jobs/', views.JobsPage),
  path('jobs-create/', views.CreateJobsPage),

  # User Login
  path('register/', UserRegistrationView.as_view(), name='register'),
  path('login/', UserLoginView.as_view(), name='login'),
  path('profile/', UserProfileView.as_view(), name='profile'),

]