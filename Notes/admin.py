from django.contrib import admin
from .models import Notes, NotesComments, Article, SiteNotes

admin.site.register(Notes)
admin.site.register(NotesComments)
admin.site.register(Article)
admin.site.register(SiteNotes)
