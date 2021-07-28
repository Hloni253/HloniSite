from django.urls import path
from .views import List_Images

urlpatterns = [
    path('List/', List_Images, name="List Images"),
    ]
