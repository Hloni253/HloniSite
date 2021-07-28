from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Images(models.Model):
    name = models.CharField(max_length=100)
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = CloudinaryField('image')

    def __str__(self):
        return self.name
