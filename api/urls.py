from django.urls import path
from .views import RegisterUser, LoginUser, LogoutUser, UserProfile, TodoListView, TodoImageView

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('profile/', UserProfile.as_view(), name='profile'),
    path('todos/', TodoListView.as_view(), name='todo-list'),
    path('todo/images/', TodoImageView.as_view(), name='todo-image'),
]