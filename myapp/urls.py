from django.urls import path
from .views import user_list,user_detail,profile_list,profile_detail,profile_city_statistics,post_list,post_detail,post_statistics_detail

urlpatterns = [
    path('users/',user_list),
    path('user/<int:pk>',user_detail),
    path('profiles/',profile_list),
    path('profile/<int:pk>',profile_detail),
    path('api/profiles/city-statistics/',profile_city_statistics),
    path('posts',post_list),
    path('posts/<int:pk>',post_detail),
    path('api/posts/<int:pk>/statistics/',post_statistics_detail),
]