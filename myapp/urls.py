from django.urls import path
from .views import user_list,user_detail,profile_list,profile_detail,profile_city_statistics,post_list,post_detail,user_statistics_detail,user_statistics,most_active_users

urlpatterns = [
    path('users/',user_list),
    path('user/<int:pk>',user_detail),
    path('profiles/',profile_list),
    path('profile/<int:pk>',profile_detail),
    path('profiles/citystatistics/',profile_city_statistics),
    path('posts',post_list),
    path('posts/<int:pk>',post_detail),
    path('users/<int:pk>/',user_statistics_detail),
    path('users/statistics/',user_statistics),
    path('users/mostactive/', most_active_users),
]