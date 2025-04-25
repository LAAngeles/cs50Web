from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    
    def __str__(self):
        return f"{self.username}"

class Like(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="like_user")
    post_id = models.IntegerField(null=True)
    likeUnlike = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.post_id}"

class Follower(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="follower_user")
    userYouFollowId = models.IntegerField(default=0)
    follow = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.userYouFollowId}"

class Post (models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="post_user")
    title = models.CharField(max_length=30)
    body = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    num_likes = models.IntegerField(default=0)
    likes= models.ManyToManyField(Like, blank=True, related_name="post_likes")

    def __str__(self):
        return f"id: {self.id}, {self.user}, likes: {self.num_likes} "
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "user_id": self.user.id,
            "title": self.title,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "num_likes": self.num_likes,
        }