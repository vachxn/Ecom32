"""
URL configuration for ecomb32 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('shop.urls')),
]

if settings.DEBUG:
    urlpatterns += path('__debug__/', include('debug_toolbar.urls')),