from django.shortcuts import render, redirect
from .models import Sites
from Home.models import Subject
from Profile.models import Profile
from django.contrib.auth.decorators import login_required
from Home.search_import import search

def List_Sites(request, subject_slug):
    subject = Subject.objects.get(slug=subject_slug)
    
    sites = Sites.objects.filter(subject=subject)

    if request.GET:
        search_query = search(request)
        sites = Sites.objects.filter(name__icontains=search_query)

    context = {
        "sites":sites,
        "subject_slug":subject_slug,
        }

    return render(request, "Sites/List_Sites.html", context)


@login_required
def Save_Site(request, site_id):
    user = request.user
    profile = Profile.objects.get(user=user)

    site = Sites.objects.get(id=site_id)

    profile.saved_sites.add(site)

    return redirect("Profile:Profile")

@login_required
def Remove_Site(request, site_id):
    profile = Profile.objects.get(user=request.user)

    site = Sites.objects.get(id=site_id)

    profile.saved_sites.remove(site)

    return redirect("Profile:Profile")
    
