"""d04 URL Configuration"""

from django.urls import path

from . import views

urlpatterns = [
    path('django/', views.django),
    path('display/', views.display),
    path('templates/', views.templates),
]
