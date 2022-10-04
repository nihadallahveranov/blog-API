from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):

    title = models.CharField(max_length = 255)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    body = models.TextField()
    likes = models.ManyToManyField(User, related_name = 'blog_posts')

    def __str__(self) -> str:
        return self.title
