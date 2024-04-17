from django.urls import path
from . import views

urlpatterns = [
    path('tweets/', views.TweetListCreateAPIView.as_view(), name='tweet-list-create'),
]
