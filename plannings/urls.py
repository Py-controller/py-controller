from django.urls import path
from . import views


urlpatterns = [
    path("planning/", views.PlanningView.as_view()),
    path("planning/<uuid:plan_uuid>/", views.PlanningDetailView.as_view()),
]
