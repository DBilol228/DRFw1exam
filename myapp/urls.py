from django.urls import path
from .views import user_list,user_detail,profile_list,profile_detail

urlpatterns = [
    path('users/',user_list),
    path('user/<int:pk>',user_detail),
    path('profiles/',profile_list),
    path('profile/<int:pk>',profile_detail),
]