from django import forms
from .models import Notes, NotesComments, SiteNotesComments


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ["name","subject","status","notes"]

class CommentsForm(forms.ModelForm):
    class Meta:
        model = NotesComments
        fields = ["comment"]


class SiteNotesCommentsForm(forms.ModelForm):
    class Meta:
        model = SiteNotesComments
        fields = ["comment"]
