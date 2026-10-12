from django.urls import path
from .views import (user_list,user_detail,profile_list,profile_detail,profile_city_statistics,post_list,
                    post_detail,user_statistics_detail,user_statistics,most_active_users,user_posts,popular_posts,
                    search_posts,filter_posts,post_statistics,author_statistics,like_list,like_delete)

urlpatterns = [
    path('users/',user_list),
    path('user/<int:pk>',user_detail),
    path('profiles/',profile_list),
    path('posts/statistics/',post_statistics),
    path('profile/<int:pk>',profile_detail),
    path('profiles/city-statistics/', profile_city_statistics),
    path('posts',post_list),
    path('posts/<int:pk>',post_detail),
    path('users/<int:pk>/',user_statistics_detail),
    path('users/statistics/',user_statistics),
    path('users/mostactive/',most_active_users),
    path('users/<int:pk>/posts/',user_posts),
    path('posts/popular/',popular_posts),
    path('posts/search/',search_posts),
    path('posts/filter/',filter_posts),
    path('posts/author-statistics/',author_statistics),
    path('likes/',like_list),
    path('likes/<int:pk>/',like_delete),
]