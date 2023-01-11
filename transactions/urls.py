from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.TransactionsView.as_view()),
    path('transactions/<str:pk>/', views.TransactionDetailView.as_view())
]
