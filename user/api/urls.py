from django.urls import path
from user.api.views import CustomUserCreate,CustomUserLogin,LogoutView


urlpatterns = [
    path('register/', CustomUserCreate.as_view(), name='register'),
    path('login/', CustomUserLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
