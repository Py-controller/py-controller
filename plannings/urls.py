from django.urls import path
from . import views


urlpatterns = [
    path("planning/<str:account_uuid>/", views.PlanningView.as_view()),
    # path("planning/<str:plan_uuid>/", views.PlanningDetailView.as_view()),
]
