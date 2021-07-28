from django.shortcuts import render
from .models import Grade, Subject



def Home(request):
    if request.user.is_authenticated:
        logged_in = True
    else:
        logged_in = False
    grades = Grade.objects.all()

    context = {
        "logged_in":logged_in,
        "grades":grades
        }

    return render(request, "Home/Home.html", context)

def List_All_Subjects(request):
    subjects = Subject.objects.all()

    context = {
        "subjects":subjects,
        }

    return render(request, "Home/List_All_Subjects.html", context)
