from django.db import models
from django.urls import reverse
from Home.models import Subject
from django.contrib.auth.models import User


class Videos(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    link = models.URLField(max_length=100)

    def __str__(self):
        return self.name

    def save_video(self):
        return reverse("Videos:Save Video", kwargs={"video_id":self.id})

    def remove_video(self):
        return reverse("Videos:Remove Video", kwargs={"video_id":self.id})
        
