from django.urls import path
from .views import List_Videos, Find_Videos, Download_Video, Save_Video, Remove_Video

app_name = "Videos"

urlpatterns = [
    path('videos/', Find_Videos, name="Find Videos"),
    path('videos/download/<video_id>', Download_Video, name="Download Video"),
    path('videos/save/<video_id>', Save_Video, name="Save Video"),
    path('videos/remove/<video_id>', Remove_Video, name="Remove Video"),
    path('videos/<subject_slug>', List_Videos, name="List Videos"),
    ]
