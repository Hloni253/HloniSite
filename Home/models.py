from django.db import models


class Grade(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    
    def __str__(self):
        return self.title

    @property
    def subjects(self):
        return self.subject_set.all()


class Subject(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, default=None)
    image = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return self.title

    def content(self):
        content = {
            "notes":"/notes/notes/site/{}".format(self.slug),
            "sites":"/sites/sites/{}".format(self.slug),
            "videos":"/videos/videos/{}".format(self.slug),
            "groups":"/profile/group/subject/{}/".format(self.slug),
            }

        return content

    @property
    def list_content(self):
        return self.content

    @property
    def list_all_notes(self):
        return self.notes_set.all()


    @property
    def list_all_groups(self):
        return self.groups_set.all()

