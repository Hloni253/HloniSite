from django.shortcuts import render, redirect
from .models import Notes, NotesComments, SiteNotes, SiteNotesComments
from .forms import NotesForm, CommentsForm, SiteNotesCommentsForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from django.views.generic import View
from .render_pdf import render_to_pdf
from Home.models import Subject
from Profile.models import Profile
from Home.search_import import search

def List_Site_Notes(request, subject_slug):
    subject = Subject.objects.get(slug=subject_slug)

    notes = SiteNotes.objects.filter(subject=subject)

    if request.GET:
        search_query = search(request)
        notes = Notes.objects.filter(name__icontains=search_query)

    context = {
        "subject":subject,
        "notes":notes,
        }

    return render(request, "Notes/List_Site_Notes.html", context)


def List_User_Notes(request, subject_slug):
    subject = Subject.objects.get(slug=subject_slug)
    
    notes = Notes.objects.filter(status="Pu", subject=subject)

    if request.GET:
        search_query = search(request)
        notes = Notes.objects.filter(name__icontains=search_query)
        

    context = {
        "subject":subject,
        "notes":notes,
        }

    return render(request, "Notes/List_Notes.html", context)

def List_Notes(request, subject_slug):
    subject = Subject.objects.get(slug=subject_slug)
    
    notes = Notes.objects.filter(status="Pu", subject=subject)

    if request.GET:
        search_query = search(request)
        notes = Notes.objects.filter(name__icontains=search_query)
        

    context = {
        "subject":subject,
        "notes":notes,
        }

    return render(request, "Notes/List_Notes.html", context)

def List_All_Notes(request):
    subjects = Subject.objects.all()

    context = {
        "subjects":subjects
        }

    return render(request, "Notes/List_All_Notes.html", context)

def View_Notes(request, note_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentsForm(request.POST)

            if form.is_valid():
                comment = NotesComments.objects.create(comment=request.POST['comment'])
                comment.note = Notes.objects.get(id=note_id)
                comment.user = request.user
                comment.save()
                return redirect("Notes:View Notes", note_id=note_id)
        else:
            return HttpResponse("<p>You have to be logged in to comment</p>")
    else:
        comments = NotesComments.objects.filter(note = Notes.objects.get(id=note_id))
        note = Notes.objects.get(id=note_id)

        if note.status == 'Pr':
            if request.user != note.user:
                return redirect('Notes:List Notes')

    context = {
        "note":note,
        "comments":comments,
        }

    return render(request, "Notes/View_Notes.html", context)


def View_Site_Notes(request, note_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = SiteNotesCommentsForm(request.POST)

            if form.is_valid():
                comment = SiteNotesComments.objects.create(comment=request.POST['comment'])
                comment.site_note = SiteNotes.objects.get(id=note_id)
                comment.user = request.user
                comment.save()
                return redirect("Notes:View Site Notes", note_id=note_id)
        else:
            return HttpResponse("<p>You have to be logged in to comment</p>")
    else:
        comments = SiteNotesComments.objects.filter(site_note = SiteNotes.objects.get(id=note_id))
        note = SiteNotes.objects.get(id=note_id)

    context = {
        "note":note,
        "comments":comments,
        }

    return render(request, "Notes/View_Site_Notes.html", context)


class View_PDF(View):
    def get(self, request, *args, **kwargs):
        note = Notes.objects.get(id=self.kwargs['note_id'])
        context = {
            "note":note
        }
        pdf = render_to_pdf('Notes/View_As_PDF.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "%s.pdf" %(note.name)
            content = "inline; filename=%s" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


class View_Site_As_PDF(View):
    def get(self, request, *args, **kwargs):
        note = SiteNotes.objects.get(id=self.kwargs['note_id'])
        context = {
            "note":note
        }
        pdf = render_to_pdf('Notes/View_Site_As_PDF.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "%s.pdf" %(note.name)
            content = "inline; filename=%s" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

@login_required
def Save_Note(request, note_id):
    note = Notes.objects.get(id=note_id)
    
    profile = Profile.objects.get(user=request.user)

    profile.copied_notes.add(note)

    return redirect("Profile:Profile")

@login_required
def Remove_Note(request, note_id):
    note = Notes.objects.get(id=note_id)
    
    profile = Profile.objects.get(user=request.user)

    profile.copied_notes.remove(note)

    return redirect("Profile:Profile")


@login_required
def Create_Note(request):
    subjects = Subject.objects.all()
    
    if request.method == "POST":
        form = NotesForm(request.POST)

        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            request.user.Note.add(item)
            return redirect('Profile:Profile')

    context = {
        "subjects":subjects,
        }

    return render(request, "Notes/Create_Note.html", context)



























