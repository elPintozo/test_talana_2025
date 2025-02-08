"""
URL configuration for talatrivia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # Para obtener el token de acceso y refresh
    TokenRefreshView,  # Para renovar el token de acceso con el refresh token
    TokenVerifyView  # Para verificar si un token es válido
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # Rutas del swagger
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    
    # Rutas de la aplicación 'trivia'
    path('api/', include('trivia.urls')),  # Incluir las rutas de la aplicación 'trivia'
    path('api/', include('equipo.urls')),  # Incluir las rutas de la aplicación 'equipo'
    
    # Rutas de autenticación
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Renovar token
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # Verificar token
]
