from django.urls import path
from . import views
from .views import BookListAPIView, BookDetail, ReviewsMyListAPIView, AuthorListAPIView
from .views import registration, review_detail, review_list
from api.views import index
urlpatterns = [
    path('', index, name='home'),
    # path('api/company', CompanyListAPIView.as_view(), name='company-list'),
    path('api/book/', BookListAPIView.as_view(), name='book-list'),
    path('api/book/<int:pk>/', BookDetail.as_view(), name='book-detail'),
    path('api/author', AuthorListAPIView.as_view(), name='author-list'),
    path('api/review/', review_list),
    path('api/review/<int:pk>/', review_detail),
    path("api/registration/", registration),

]
