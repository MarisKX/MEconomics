"""
URL mappings for the companies app
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from companies import views

router = DefaultRouter()
router.register('companies', views.CompanyViewSet)
router.register('governmentinstitutions', views.GovermentInstViewSet)

app_name = 'companies'

urlpatterns = [
    path('', include(router.urls))
]
