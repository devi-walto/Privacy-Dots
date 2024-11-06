from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path('motion/', views.motion_detected, name='motion_detected'),
]
