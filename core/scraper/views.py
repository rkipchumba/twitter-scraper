from rest_framework import generics
from .models import Tweet
from .serializers import TweetSerializer
from rest_framework.pagination import PageNumberPagination

class TweetPagination(PageNumberPagination):
    page_size = 10

class TweetListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    pagination_class = None  # Disable pagination for now

class SavedPostListView(generics.ListAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    pagination_class = TweetPagination
