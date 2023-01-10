from django.contrib import admin
from django.urls import path
from .views import UserView, UserDetailView, PersonalizedTokenObtainPairView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("users/", UserView.as_view()),
    path("users/<str:user_uuid>/", UserDetailView.as_view()),
    path("login/", PersonalizedTokenObtainPairView.as_view()),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
