from django.shortcuts import render
from .models import Images

def List_Images(request):
    images = Images.objects.all()

    context = {
        "images":images,
        }
    
    return render(request, "Images/List_Images.html", context)
