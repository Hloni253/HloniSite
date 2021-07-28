from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from Home.models import Subject
from django.urls import reverse
from Notes.models import Notes
from Videos.models import Videos
from Sites.models import Sites


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField()
    description = models.CharField(max_length=500, blank=True)
    copied_notes = models.ManyToManyField(Notes, blank=True, related_name="Notes")
    saved_videos = models.ManyToManyField(Videos,blank=True,related_name="Videos")
    saved_sites = models.ManyToManyField(Sites, blank=True, related_name="Sites")
    groups = models.ManyToManyField("Groups", blank=True, related_name="UserGroups")
    
    
    def __str__(self):
        return str(self.user.username)


def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance, slug=instance)
        except:
            pass
        
post_save.connect(create_profile, sender=User)

class Groups(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="GroupCreator")
    members = models.ManyToManyField(User, blank=True, related_name="GroupMembers")
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.ManyToManyField(Notes, blank=True, related_name="GroupNotes")
    sites = models.ManyToManyField(Sites, blank=True, related_name="GroupSites")
    videos = models.ManyToManyField(Videos, blank=True, related_name="GroupVideos")

    def __str__(self):
        return self.name

    def add_note(self):
        return reverse("Profile:Select Content", kwargs={"content_slug":"note", "group_id":self.id})

    def add_site(self):
        return reverse("Profile:Select Content", kwargs={"content_slug":"site", "group_id":self.id})

    def add_video(self):
        return reverse("Profile:Select Content", kwargs={"content_slug":"video", "group_id":self.id})



class GroupComments(models.Model):
    user = models.ForeignKey(User, related_name="GroupCommentUser", on_delete=models.CASCADE, default=None)
    comment = models.TextField()
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} Comment On Group {} id{}".format(self.user.username, self.group.name,self.id)

    def first_fifty_words(self):
        return self.comment[0:50]





















    
