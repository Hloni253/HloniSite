from django.contrib import admin
from .models import Profile, Groups, GroupComments

admin.site.register(Profile)
admin.site.register(Groups)
admin.site.register(GroupComments)
