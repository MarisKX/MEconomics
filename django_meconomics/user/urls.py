"""
URL mappings for the user API
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user import views


router = DefaultRouter()
router.register('all-users', views.AllUsersView)

app_name = 'user'

urlpatterns = [
    path('', include(router.urls)),
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('check-auth/', views.CheckAuth.as_view(), name='check-auth'),
    path('log-out/', views.LogoutView.as_view(), name='log-out'),
]
