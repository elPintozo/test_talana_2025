from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from equipo.models import Trabajador
from equipo.serializers import TrabajadorSerializer
from django.shortcuts import get_object_or_404

class TrabajadorAPI(APIView):

    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados
    
    def get(self, request, pk=None):
        """
        Obtiene un trabajador por su id o todos las trabajadores
        """
        if pk:
            trabajador = get_object_or_404(Trabajador, pk=pk)
            serializer = TrabajadorSerializer(trabajador)
        else:
            trabajadores = Trabajador.objects.filter(user__is_superuser=False)
            serializer = TrabajadorSerializer(trabajadores, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """
        Crea un nuev trabajador
        """
        serializer = TrabajadorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Actualiza un trabajador
        """
        trabajador = get_object_or_404(Trabajador, pk=pk)
        serializer = TrabajadorSerializer(trabajador, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Elimina un trabajador
        """
        trabajador = get_object_or_404(Trabajador, pk=pk)
        trabajador.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TrabajadorAdministradorAPI(APIView):

    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados
    
    def get(self, request, pk=None):
        """
        Obtiene un administrador por su id o todos las adminitradores
        """
        if pk:
            trabajador = get_object_or_404(Trabajador, pk=pk)
            serializer = TrabajadorSerializer(trabajador)
        else:
            trabajadores = Trabajador.objects.filter(user__is_superuser=True)
            serializer = TrabajadorSerializer(trabajadores, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """
        Crea un nuev trabajador
        """
        serializer = TrabajadorSerializer(data=request.data)
        if serializer.is_valid():

            nuevo_adminitrador = serializer.save()
            nuevo_adminitrador.user.is_staff = True
            nuevo_adminitrador.user.is_superuser = True
            nuevo_adminitrador.user.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
