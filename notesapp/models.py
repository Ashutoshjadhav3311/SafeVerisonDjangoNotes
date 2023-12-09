from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # user name defines the notes of the user to show
    STATUS = (
        ("new", "NEWEST"),
        ("old", "OLDEST"),
        ("title", "TITLE"),
    )
    heading = models.CharField(max_length=200)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS, default="old")
    
    
    def __str__(self):
        return self.heading
class Revision(models.Model):
    note = models.ForeignKey(Notes, on_delete=models.CASCADE)
    revision_date = models.DateTimeField()

    def __str__(self):
        return f"Revision for {self.note.heading} on {self.revision_date}"

    
class RevisionCheckbox(models.Model):
    revision = models.ForeignKey(Revision, on_delete=models.CASCADE)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return f"Checkbox for {self.revision}"