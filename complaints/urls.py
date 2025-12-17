from django.urls import path
from .views import (
    dashboard, complaint_create, complaint_list, complaint_detail,
    complaint_assign, complaint_update
)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('complaints/', complaint_list, name='list'),
    path('complaints/new/', complaint_create, name='create'),
    path('complaints/<int:pk>/', complaint_detail, name='detail'),
    path('complaints/<int:pk>/assign/', complaint_assign, name='assign'),
    path('complaints/<int:pk>/update/', complaint_update, name='update'),
]