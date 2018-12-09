from django.urls import path
from rooms import views

urlpatterns = [
    path('rooms/', views.room_list),
    path('rooms/<int:pk>/', views.room_detail),
    path('enter/', views.enter_occupant),
    path('exit/', views.exit_occupant),
]
