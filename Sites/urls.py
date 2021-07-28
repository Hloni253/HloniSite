from django.urls import path
from .views import List_Sites, Save_Site, Remove_Site

app_name = "Sites"

urlpatterns = [
    path('sites/<subject_slug>', List_Sites, name="List Sites"),
    path('sites/save/<site_id>', Save_Site, name="Save Site"),
    path('sites/remove/<site_id>', Remove_Site, name="Remove Site"),
    ]
