from django.urls import path
from . import views

urlpatterns = [
    path("accounts/", views.AccountView.as_view()),
    path("accounts/<str:account_uuid>/", views.AccountDetailView.as_view()),
    # path("accounts/<str:account_uuid>/transactions", views.AccountTransactionView.as_view()),
    # path("accounts/<str:account_uuid>/plannings", views.AccountPlanningView.as_view()),
]
