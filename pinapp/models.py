from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    following = models.ManyToManyField(
        "self",
        through="Follow",
        related_name="following_by",
        symmetrical=False,
        # blank=True,
    )
    followers = models.ManyToManyField(
        "self",
        through="Follow",
        related_name="followed_by",
        symmetrical=False,
        # blank=True,
    )

    def __str__(self):
        return self.user.username


class Follow(models.Model):
    follower = models.ForeignKey(
        "UserProfile", related_name="following_relations", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        "UserProfile", related_name="follower_relations", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")

    def __str__(self):
        return f"{self.follower.user.username} follows {self.following.user.username}"
