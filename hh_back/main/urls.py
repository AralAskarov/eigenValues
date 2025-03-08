from django.urls import path
from . import views
from main.views import hello, about

urlpatterns = [
    path('index/', views.index, name = 'home'),
    path('hi/', hello),
    path('about/', about),
    
]
