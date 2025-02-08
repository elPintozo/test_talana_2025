from django.urls import path
from equipo.api.api_trabajador import (
    TrabajadorAPI,
    TrabajadorDetalleAPI,
    TrabajadorAdministradorAPI,
    TrabajadorAdministradorDetalleAPI
)

urlpatterns = [
    path('trabajador/', TrabajadorAPI.as_view(), name='trabajador-crear-listar'),  # Listar y crear trabajadores
    path('trabajador/<int:pk>/', TrabajadorDetalleAPI.as_view(), name='trabajador-actualizar'),  # Obtener, actualizar y eliminar un trabajador específico

    path('trabajador/administrador/', TrabajadorAdministradorAPI.as_view(), name='administrador-crear-listar'),  # Listar y crear administradores
    path('trabajador/administrador/<int:pk>/', TrabajadorAdministradorDetalleAPI.as_view(), name='administrador-actualizar'),  # Obtener, actualizar y eliminar un administrador específico
]