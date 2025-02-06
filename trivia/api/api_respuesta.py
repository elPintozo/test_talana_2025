from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from trivia.models import Respuesta
from trivia.serializers import RespuestaSerializer
from django.shortcuts import get_object_or_404

class RespuestaAPI(APIView):
    
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados

    def get(self, request, pk=None):
        """
        Obtiene una respuesta por su id o todas las respuestas
        """
        print( '-> get:', pk)
        if pk:
            respuesta = get_object_or_404(Respuesta, pk=pk)
            serializer = RespuestaSerializer(respuesta)
        else:
            respuestas = Respuesta.objects.all()
            serializer = RespuestaSerializer(respuestas, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """
        Crea una nueva respuesta
        """
        print( '-> post:', request.data)
        serializer = RespuestaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Actualiza una respuesta
        """
        print( '-> put:', request.data, pk)
        respuesta = get_object_or_404(Respuesta, pk=pk)
        serializer = RespuestaSerializer(respuesta, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Elimina una respuesta
        """
        print( '-> delete:', pk)
        respuesta = get_object_or_404(Respuesta, pk=pk)
        respuesta.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)