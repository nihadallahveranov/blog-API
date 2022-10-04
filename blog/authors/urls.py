from django.urls import include, path
from django.contrib import admin

from .views import RegisterView, UserView, UserDetailView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('', UserView.as_view(), name='authors'),
    path('<int:pk>', UserDetailView.as_view(), name = 'author-detail'),
]