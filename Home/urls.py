from django.urls import path
from .views import Home

app_name = "Home"

urlpatterns = [
    path('', Home, name="Home"),
    ]
