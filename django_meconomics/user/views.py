"""
Views for the user API
"""
# Django/DRF imports
from rest_framework import (
    generics,
    authentication,
    permissions,
    status,
    viewsets
)
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.views import APIView, View
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.middleware.csrf import get_token as get_csrf_token
# Model imports
from core.models import User, AppSettings
# Serializer imports
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    AppSettingsSerializer,
    AppSettingsDetailSerializer,
)
# Custom imports
from core.custom_functions.today import today


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        csrf_token = get_csrf_token(request)

        response_data = {
            'user_id': user.pk,
            'username': user.email,
            'token': token.key,
        }

        response = Response(response_data)
        response.set_cookie(
            'auth_token',
            token.key,
            domain='meconomics.com',  # Add this line to allow subdomain access
            httponly=True,
            samesite='Lax',
        )
        response.set_cookie(
            'csrftoken',
            csrf_token,
            domain='meconomics.com',
            httponly=False,
            samesite='Lax',
        )

        return response


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authentcated user"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class CheckAuth(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_token_from_cookie(self, request):
        return request.COOKIES.get('auth_token')

    def get(self, request):
        auth_token = request.META.get("HTTP_AUTHORIZATION")
        cookie_token = self.get_token_from_cookie(request)

        # Check for the token in the cookie or header
        if auth_token and "Token" in auth_token:
            token_key = auth_token.split(" ")[1]
        elif cookie_token:
            token_key = cookie_token
        else:
            return JsonResponse(
                {"authenticated": False, "username": None},
                status=status.HTTP_401_UNAUTHORIZED)

        try:
            token_obj = Token.objects.get(key=token_key)
            user = token_obj.user
            username = user.email
            current_date = today().strftime("%d-%m-%Y")

        except Token.DoesNotExist:
            return JsonResponse(
                {"authenticated": False, "username": None},
                status=status.HTTP_401_UNAUTHORIZED)

        return JsonResponse({
            "authenticated": True,
            "username": username,
            "dateToday": current_date,
        })


class LogoutView(View):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        # Delete the auth_token cookie
        response = JsonResponse({"message": "Logged out successfully"})
        response.set_cookie(
            'auth_token',
            '',
            expires='Thu, 01 Jan 1970 00:00:01 GMT',  # This is in the past
            domain='.maris.com',  # Add this line to allow subdomain access
            httponly=True,
            samesite='Lax',
        )
        return response


class AllUsersView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        queryset = User.objects.all()

        user_id = self.request.query_params.get('truck_id_user')
        print(user_id)
        if user_id is not None:
            queryset = queryset.filter(id=user_id)

        return queryset


class AppSettingsViewSet(viewsets.ModelViewSet):
    """View for manage App Settings"""
    serializer_class = AppSettingsDetailSerializer
    queryset = AppSettings.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return the srializer class for company"""
        if self.action == 'list':
            return AppSettingsSerializer

        return self.serializer_class

    def get_queryset(self):
        """Retrieve App Settings"""
        queryset = self.queryset
        return queryset.filter().order_by('-id')

    def perform_create(self, serializer):
        """Create a new company"""
        serializer.save()
