from __future__ import absolute_import, unicode_literals

from celery import shared_task

from .models import Post

@shared_task
def unlike_posts():
    posts = Post.objects.all()

    for post in posts:
        post.likes.clear()
        
    post.save()
    print(f'all post likes deleted successfully')    