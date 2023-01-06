from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.ListCreateTransactions.as_view()),
    path('transactions/<str:pk>/', views.RetrieveUpdateDestroyTransaction.as_view())
]