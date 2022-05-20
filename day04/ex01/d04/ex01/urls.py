"""d04 URL Configuration"""

from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('django/', views.django),
]
