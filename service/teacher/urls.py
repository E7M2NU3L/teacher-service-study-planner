from django.urls import path
from teacher import views

urlpatterns = [
    path('initialize', views.Create_RAG),
    path('invoke', views.AskQuestion)
]