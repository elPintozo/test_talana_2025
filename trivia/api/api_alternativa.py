from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from trivia.models import Pregunta, Alternativa
from trivia.serializers import AlternativaSerializer
from django.shortcuts import get_object_or_404

class AlternativaAPI(APIView):

    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados
    
    def get(self, request, pk=None):
        """
        Obtiene una alternativa por su id o todas las alternativas
        """
        print( '-> get:', pk)
        if pk:
            alternativa = get_object_or_404(Alternativa, pk=pk)
            serializer = AlternativaSerializer(alternativa)
        else:
            alternativas = Alternativa.objects.all()
            serializer = AlternativaSerializer(alternativas, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Crea una nueva alternativa
        """
        print( '-> post:', request.data)
        serializer = AlternativaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Actualiza una alternativa
        """
        print( '-> put:', request.data, pk)
        alternativa = get_object_or_404(Alternativa, pk=pk)
        serializer = AlternativaSerializer(alternativa, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Elimina una alternativa
        """
        print( '-> delete:', pk)
        alternativa = get_object_or_404(Alternativa, pk=pk)
        alternativa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AlternativasPorPreguntaAPI(APIView):

    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados

    def get(self, request, pregunta_id):
        pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
        alternativas = Alternativa.objects.filter(pregunta=pregunta)
        serializer = AlternativaSerializer(alternativas, many=True)
        return Response(serializer.data)
