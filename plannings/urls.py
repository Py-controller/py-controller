from django.urls import path
from . import views


urlpatterns = [
    path("planning/create/<str:account_uuid>/", views.PlanningCreateView.as_view()),
    path("planning/", views.PlanningListView.as_view()),
    path("planning/<str:plan_uuid>/", views.PlanningDetailView.as_view()),
]
