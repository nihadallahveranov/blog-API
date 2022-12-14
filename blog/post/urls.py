from django.urls import path
from .views import PostView, PostDetailView, PostDeleteView, PostLikesView

urlpatterns = [
    path('', PostView.as_view(), name = 'home'),
    path('post/<int:pk>', PostDetailView.as_view(), name = 'post-detail'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name = 'post-delete'),
    path('post/<int:pk>/likes', PostLikesView.as_view(), name = 'post-likes'),
]