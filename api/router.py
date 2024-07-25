from django.urls import path
from .views import *

urlpatterns = [
    path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-retrieve-update-destroy'),
    
    path('kids/', KidListCreateAPIView.as_view(), name='kid-list-create'),
    path('kids/<int:pk>/', KidRetrieveUpdateDestroyAPIView.as_view(), name='kid-retrieve-update-destroy'),
    
    path('teachers/', TeacherListCreateAPIView.as_view(), name='teacher-list-create'),
    path('teachers/<int:pk>/', TeacherRetrieveUpdateDestroyAPIView.as_view(), name='teacher-retrieve-update-destroy'),
    
    path('groups/', GroupListCreateAPIView.as_view(), name='group-list-create'),
    path('groups/<int:pk>/', GroupRetrieveUpdateDestroyAPIView.as_view(), name='group-retrieve-update-destroy'),
    
    path('journals/', JournalListCreateAPIView.as_view(), name='journal-list-create'),
    path('journals/<int:pk>/', JournalRetrieveUpdateDestroyAPIView.as_view(), name='journal-retrieve-update-destroy'),
]
