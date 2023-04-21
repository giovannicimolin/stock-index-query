"""
URL configuration for stock_query_index project.
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from stock_data import views

router = DefaultRouter()
router.register(r"ticker", views.TickerViewset, basename="ticker")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
]
