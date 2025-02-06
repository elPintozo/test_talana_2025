from django.urls import path
from equipo.api.api_trabajador import TrabajadorAPI, TrabajadorAdministradorAPI

urlpatterns = [
    path('trabajador/', TrabajadorAPI.as_view(), name='trabajador-crear-listar'),  # Listar y crear trabajadores
    path('trabajador/<int:pk>/', TrabajadorAPI.as_view(), name='trabajador-actualizar'),  # Obtener, actualizar y eliminar un trabajador específico

    path('trabajador/administrador/', TrabajadorAdministradorAPI.as_view(), name='administrador-crear-listar'),  # Listar y crear administradores
    path('trabajador/administrador/<int:pk>/', TrabajadorAdministradorAPI.as_view(), name='administrador-actualizar'),  # Obtener, actualizar y eliminar un administrador específico
]