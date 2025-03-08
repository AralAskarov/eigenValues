from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Book, Review, Author
from api.serializers import BookSerializer, AuthorSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics


class BookListAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
class BookDetail(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class=BookSerializer
    permission_classes = [AllowAny]

class AuthorListAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]

class ReviewsMyListAPIView(generics.ListCreateAPIView):
    # queryset = Company.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




