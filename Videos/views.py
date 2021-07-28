from django.shortcuts import render, redirect
from .models import Videos
from Home.models import Subject
from Home.search_import import search
from youtube_search import YoutubeSearch
from django.contrib.auth.decorators import login_required
from Profile.models import Profile



def List_Videos(request, subject_slug):
    subject = Subject.objects.get(slug=subject_slug)
    
    videos = Videos.objects.filter(subject=subject)

    if request.GET:
        search_term = search(request)
        videos = Videos.objects.filter(name__icontains=search_term)

    context = {
        "videos":videos,
        }

    return render(request, "Videos/List_Videos.html", context)


def Find_Videos(request):
    videos = False
    videos_dict = {}

    if request.GET:
        videos = True
        search_term = search(request)
        results = YoutubeSearch(search_term, max_results=10).to_dict()
        for result in results:
            videos_dict[result['title']] = result['url_suffix']

    context = {
        "videos":videos,
        "videos_dict":videos_dict,
        }            

    return render(request, "Videos/Find_Video.html", context)

def Download_Video(request, video_id):
    verification_url = ["https://www.youtube.com"]
    video = Videos.objects.get(id=video_id)

    for url in verification_url:
        if video.link.startswith(url):
            video_link = video.link.replace(url,"")
            break
        

    download_url = "https://youtubepp.com{}".format(video_link)

    return redirect(download_url)
  


@login_required
def Save_Video(request, video_id):
    video = Videos.objects.get(id=video_id)
    
    profile = Profile.objects.get(user=request.user)

    profile.saved_videos.add(video)

    return redirect("Profile:Profile")

@login_required
def Remove_Video(request, video_id):
    video = Videos.objects.get(id=video_id)

    profile = Profile.objects.get(user=request.user)

    profile.saved_videos.remove(video)

    return redirect("Profile:Profile")























