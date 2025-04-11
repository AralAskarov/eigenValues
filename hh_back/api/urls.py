from django.urls import path
from . import views
from .views import BookListAPIView, BookDetail, ReviewsMyListAPIView, AuthorListAPIView, UserPreferencesView, GlobalPreferencesView
from .views import registration, review_detail, review_list, profile, get_recommendations, search_books
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
    path('api/profile/', profile, name='profile'),
    path('get_recommendations', get_recommendations, name='get_recommendations'),
    # Путь для предпочтений пользователя
    path('user/<int:user_id>/preferences/', views.UserPreferencesView.as_view(), name='user-preferences'),
    path('global/preferences/', views.GlobalPreferencesView.as_view(), name='global-preferences'),
    path('api/search_books/', search_books, name='search_books'),


]
