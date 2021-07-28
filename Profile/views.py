from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Profile, Groups, GroupComments
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from Notes.models import Notes
from Videos.models import Videos
from Sites.models import Sites
from Home.models import Subject
from Home.search_import import search

def username_exists(username):
    if User.objects.filter(username=username).exists():
        return True

    return False

def Register(request):
    if request.method == "POST":

        username = request.POST['username']

        if username_exists(username):
            return HttpResponse("<p>A user with that username already exists. <br>Try another username</p>")

        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            user = User.objects.create_user(request.POST['username'])
            user.set_password(request.POST['password1'])
            user.save()

            login(request, user)

            return redirect('Profile:Profile')

        else:
            return HttpResponse("<p>Your Passwords are not the same please register again</p>")

    return render(request, 'Profile/Register.html')

def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if username_exists(username):

            user = User.objects.get(username=username)

            confirm_password = user.password

            if check_password(password,confirm_password):
                login(request,user)
                return redirect('Profile:Profile')

            else:
                return HttpResponse("<p>Please try to login again</p>")
        else:
            return HttpResponse("<p>The user you logged in with does not exist please register</p>")

    return render(request, 'Profile/login.html')

@login_required
def User_Profile(request):

    user = request.user
    
    profile = Profile.objects.get(user=user)

    saved_notes = profile.copied_notes.all()

    notes = Notes.objects.filter(user=user)

    sites = profile.saved_sites.all()

    videos = profile.saved_videos.all()

    groups = Groups.objects.filter(creator=user or user in members)

    if request.GET:
        search_term = search(request)
        notes = notes.filter(name__icontains=search_term)
        saved_notes = saved_notes.filter(name__icontains=search_term)
        sites = sites.filter(name__icontains=search_term)
        videos = videos.filter(name__icontains=search_term)
        groups = groups.filter(name__icontains=search_term)

    context = {
        "profile":profile,
        "saved_notes":saved_notes,
        "notes":notes,
        "sites":sites,
        "videos":videos,
        "groups":groups,
        }

    
    return render(request, "Profile/Profile.html",context)

@login_required
def Add_Description(request):
    profile = Profile.objects.get(user=request.user)

    if request.POST:
        description = request.POST['description']

        profile.description = description

        profile.save()

        return redirect("Profile:Profile")

    return render(request, "Profile/Add_Description.html")



def View_Profile(request, profile_slug):
    profile = Profile.objects.get(slug=profile_slug)

    notes = Notes.objects.filter(user=profile.user,status="Pu")

    videos = profile.saved_videos.all()

    sites = profile.saved_sites.all()

    saved_notes = profile.copied_notes.all()

    groups = Groups.objects.filter(members = profile.user)

    context = {
        "profile":profile,
        "saved_notes":saved_notes,
        "videos":videos,
        "sites":sites,
        "notes":notes,
        "groups":groups,
        }

    return render(request, "Profile/ViewProfile.html",context)

def List_All_Groups(request):
    groups = Groups.objects.all()

    if request.GET:
        search_query = request.GET.get("search")
        groups = Groups.objects.filter(name__icontains=search_query)

    context = {
        "groups":groups
        }

    return render(request, "Profile/List_All_Groups.html", context)


def List_Subject_Groups(request, subject_slug):
    subject = Subject.objects.get(slug=subject_slug)

    context = {
        "subject":subject,
        }

    return render(request, "Profile/List_Subject_Groups.html", context)


def View_Group(request, group_id):
    group = Groups.objects.get(id=group_id)

    comments = GroupComments.objects.filter(group=group)

    context = {
        "group":group,
        "comments":comments,
        }

    return render(request, "Profile/View_Group.html", context)


@login_required
def Create_Group(request):
    user = request.user
    subjects = Subject.objects.all()

    if request.POST:
        group_name = request.POST['name']
        group_description = request.POST['description']
        group_subject_id = request.POST['subject']

        group_subject = Subject.objects.get(id=group_subject_id)

        group = Groups.objects.create(name=group_name,description=group_description,creator=user,subject=group_subject)
        group.members.add(user)
        group.save()

        return redirect("Profile:View Group", group_id=group.id)

    context = {
        "subjects":subjects,
         }

    return render(request, "Profile/Create_Group.html", context)



@login_required
def Join_Group(request, group_id):
    user = request.user

    if Groups.objects.get(id=group_id):
        group = Groups.objects.get(id=group_id)

        group.members.add(user)
        group.save()

        profile = Profile.objects.get(user=user)
        profile.groups.add(group)
        profile.save()

        return redirect("Profile:View Group",group_id=group_id)
    else:
        return redirect("Home:Home")

def List_All_Group_Members(request,group_id):
    group = Groups.objects.get(id=group_id)

    group_members = group.members.all()

    if request.GET:
        search_term = search(request)
        group_members = group_members.filter(username__icontains=search_term)

    context = {
        "group":group,
        "group_members":group_members,
        }

    return render(request, "Profile/List_All_Group_Members.html", context)

@login_required
def Write_Comment(request, group_id):
    group = Groups.objects.get(id=group_id)

    if request.POST:
        comment = request.POST['comment']
        group_comment = GroupComments.objects.create(user=request.user,comment=comment, group=group)
        group_comment.save()

        return redirect("/profile/group/{}#GroupComment".format(group_id))

    context = {
        "group":group
        }

    return render(request, "Profile/Write_Comment.html", context)


@login_required
def Select_Group_Content(request, content_slug, group_id):
    site_user = request.user

    if Groups.objects.get(id=group_id):
        group = Groups.objects.get(id=group_id)

        if site_user in group.members.all():
            notes = None
            sites = None
            videos = None
            profile = Profile.objects.get(user=site_user)
            
            if content_slug == "note":
                notes = Notes.objects.filter(user=site_user)

            elif content_slug == "site":
                sites = profile.saved_sites.all()

            elif content_slug == "video":
                videos = profile.saved_videos.all()
                
            else:
                return redirect("Home:Home")

            context = {
                "notes":notes,
                "sites":sites,
                "videos":videos,
                "group":group,
                "profile":profile,
                 }

            return render(request, "Profile/Select_Group.html", context)

        else:
            return redirect("Profile:Profile")

    else:
        return redirect("Profile:Profile")

@login_required
def Select_Note(request, group_id, note_id):
    group = Groups.objects.get(id=group_id)

    note = Notes.objects.get(id=note_id)

    group.notes.add(note)

    return redirect("/profile/group/{}#GroupNotes".format(group_id))

    

@login_required
def Select_Video(request, group_id, video_id):
    group = Groups.objects.get(id=group_id)

    video = Videos.objects.get(id=video_id)

    group.videos.add(video)

    return redirect("/profile/group/{}#GroupVideos".format(group_id))

@login_required
def Select_Site(request, group_id, site_id):
    group = Groups.objects.get(id=group_id)

    site = Sites.objects.get(id=site_id)

    group.sites.add(site)

    return redirect("/profile/group/{}#GroupSites".format(group_id))






























