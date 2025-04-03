from django.urls import path
from .views import (UserDetailView, UserListView, UserRegisterView, UserUpdateView, CustomLoginView)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Login y Logout
    path('login/', CustomLoginView.as_view(template_name="users/login.html"), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    
    # User routes
    path('', UserListView.as_view(), name= "user_list"),
    path('profile/', UserDetailView.as_view(), name= "user_detail"),
    path('edit-profile/', UserUpdateView.as_view(), name= "user_edit"),
    path('register/', UserRegisterView.as_view(), name= "user_register"),
]