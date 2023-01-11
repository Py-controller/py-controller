from django.urls import path
from . import views

urlpatterns = [
    path("addresses/", views.AddressView.as_view()),
]
