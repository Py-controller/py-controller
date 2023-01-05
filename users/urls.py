from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import UserView, UserDetailView

urlpatterns = [
    path("users/", UserView.as_view()),
    path("users/<str:user_uuid>/", UserDetailView.as_view()),
    path("login/", TokenObtainPairView.as_view()),
]
