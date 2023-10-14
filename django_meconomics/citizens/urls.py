"""
URL mappings for the recipe app
"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from citizens import views

router = DefaultRouter()
router.register('citizens', views.CitizenViewSet)

app_name = 'citizens'

urlpatterns = [
    path('', include(router.urls))
]
