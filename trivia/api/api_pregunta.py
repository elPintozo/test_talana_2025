from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from trivia.models import Pregunta
from trivia.serializers import PreguntaSerializer
from django.shortcuts import get_object_or_404

class PreguntaAPI(APIView):
    
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados

    def get(self, request, pk=None):
        """
        Obtiene una pregunta por su id o todas las preguntas
        """
        print( '-> get:', pk)
        if pk:
            pregunta = get_object_or_404(Pregunta, pk=pk)
            serializer = PreguntaSerializer(pregunta)
        else:
            preguntas = Pregunta.objects.all()
            serializer = PreguntaSerializer(preguntas, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """
        Crea una nueva pregunta
        """
        print( '-> post:', request.data)
        serializer = PreguntaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Actualiza una pregunta
        """
        print( '-> put:', request.data, pk)
        pregunta = get_object_or_404(Pregunta, pk=pk)
        serializer = PreguntaSerializer(pregunta, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Elimina una pregunta
        """
        print( '-> delete:', pk)
        pregunta = get_object_or_404(Pregunta, pk=pk)
        pregunta.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
