from django.urls import path
from .views import *

urlpatterns = [
    
    path('kids/', KidListCreateAPIView.as_view(), name='kid-list-create'),
    path('kids/<int:pk>/', KidRetrieveUpdateDestroyAPIView.as_view(), name='kid-retrieve-update-destroy'),
    path('month-archives/<int:pk>/', MonthArchiveRetrieveUpdateDestroyAPIView.as_view(), name='month-archive-retrieve-update'),

    path('income-transactions/', IncomeTransactionListCreateAPIView.as_view(), name='income-transaction-list-create'),
    path('income-transactions/<int:pk>/', IncomeTransactionRetrieveUpdateDestroyAPIView.as_view(), name='income-transaction-retrieve-update-destroy'),
    
    path('stuff/', StaffListAPIView.as_view(), name='staff-list'),
    path('stuff/<int:pk>/', StuffDetailAPIView.as_view(), name='stuff-detail'),

    path('groups/', GroupListCreateAPIView.as_view(), name='group-list-create'),
    path('groups/<int:pk>/', GroupRetrieveUpdateDestroyAPIView.as_view(), name='group-retrieve-update-destroy'),



    path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-retrieve-update-destroy'),
    path('journals/', JournalListCreateAPIView.as_view(), name='journal-list-create'),
    path('journals/<int:pk>/', JournalRetrieveUpdateDestroyAPIView.as_view(), name='journal-retrieve-update-destroy'),
]
