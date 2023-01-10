from django.urls import path
from . import views


urlpatterns = [
    path('reports/', views.ReportView.as_view()),
    # path('reports/accounts/<str:account_uuid>', views.AccountReportsView.as_view()),
    path('reports/plannings/<str:plainning_uuid>/', views.ReportPlainingsView.as_view()),
]
