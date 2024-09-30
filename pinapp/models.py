from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    

    def __str__(self):
        return self.user.username
