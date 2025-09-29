from django.contrib import admin
from django.urls import path
from email_classifier import views
from core.api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
    path('', views.index, name='index'),
]
