from django.db import models
from Home.models import Subject
from django.urls import reverse
from django.contrib.auth.models import User


class Sites(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    link = models.URLField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def save_site(self):
        return reverse("Sites:Save Site", kwargs={"site_id":self.id})

    def remove_site(self):
        return reverse("Sites:Remove Site", kwargs={"site_id":self.id})

