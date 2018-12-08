from django.urls import path
from rooms import views

urlpatterns = [
    path('rooms/', views.room_list),
    path('rooms/<int:pk>/', views.room_detail),
]
