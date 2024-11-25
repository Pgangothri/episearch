from django.urls import path, include
from .views import suggestion, search_recipes_api 

urlpatterns = [
    path('suggestion/', suggestion),
    path('search/', search_recipes_api),
]