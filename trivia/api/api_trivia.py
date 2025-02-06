from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from trivia.models import Trivia
from trivia.serializers import TriviaSerializer
from django.shortcuts import get_object_or_404

class TriviaAPI(APIView):
    
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados

    def get(self, request, pk=None):
        """
        Obtiene una trivia por su id o todas las trivias
        """
        print( '-> get:', pk)
        if pk:
            trivia = get_object_or_404(Trivia, pk=pk)
            serializer = TriviaSerializer(trivia)
        else:
            trivias = Trivia.objects.all()
            serializer = TriviaSerializer(trivias, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """
        Crea una nueva trivia
        """
        print( '-> post:', request.data)
        serializer = TriviaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Actualiza una trivia
        """
        print( '-> put:', request.data, pk)
        trivia = get_object_or_404(Trivia, pk=pk)
        serializer = TriviaSerializer(trivia, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Elimina una trivia
        """
        print( '-> delete:', pk)
        trivia = get_object_or_404(Trivia, pk=pk)
        trivia.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)