from django.urls import path
from . import views

urlpatterns = [
    path('event/hook/', views.event_hook, name='event_hook'),
]
