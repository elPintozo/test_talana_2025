from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from trivia.models import Trivia
from django.http import Http404
from trivia.serializers import TriviaSerializer
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiTypes, OpenApiExample


class TriviaAPI(APIView):
    
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados

    @extend_schema(
        summary="Todas las trivias",
        responses={200: TriviaSerializer(many=True)},
    )
    def get(self, request):
        trivias = Trivia.objects.all()
        serializer = TriviaSerializer(trivias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary="Crea una nueva trivia",
        request=TriviaSerializer,
        parameters=[
            OpenApiParameter(
                name="nombre",
                description="Nombre de la trivia",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="descripcion",
                description="Descripción de la trivia",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="preguntas",
                description="Lista de IDs de preguntas",
                required=False,
                type={'type': 'array', 'items': {'type': 'number'}}
            ),
            OpenApiParameter(
                name="trabajadores",
                description="Lista de IDs de trabajadores",
                required=False,
                type={'type': 'array', 'items': {'type': 'number'}}
            ),
        ],
        responses={
            201: TriviaSerializer,
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Error de validación",
                examples=[
                    OpenApiExample(
                        name="Ejemplo de error",
                        description="Este es un error de validación cuando el campo 'nombre' está vacío.",
                        value={"nombre": ["This field is required."]},
                        response_only=True,  # Indica que este ejemplo es solo para respuestas
                    ),
                    OpenApiExample(
                        name="Ejemplo de error",
                        description="Este es un error de validación cuando el campo 'descripcion' está vacío.",
                        value={"descripcion": ["This field is required."]},
                        response_only=True,  # Indica que este ejemplo es solo para respuestas
                    )
                ],
            ),
        },
    )
    def post(self, request):
        serializer = TriviaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TriviaDetalleAPI(APIView):
    
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados

    @extend_schema(
        summary="Obtiene una trivia",
        responses={
            200: TriviaSerializer,
            404: OpenApiResponse(response=OpenApiTypes.OBJECT),
        }
    )
    def get(self, request, pk=None):
        if pk:
            trivia = get_object_or_404(Trivia, pk=pk)
            serializer = TriviaSerializer(trivia)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Actualiza una trivia",
        request=TriviaSerializer,
        parameters=[
            OpenApiParameter(
                name="nombre",
                description="Nombre de la trivia",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="descripcion",
                description="Descripción de la trivia",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="preguntas",
                description="Lista de IDs de preguntas",
                required=False,
                type={'type': 'array', 'items': {'type': 'number'}}
            ),
            OpenApiParameter(
                name="trabajadores",
                description="Lista de IDs de trabajadores",
                required=False,
                type={'type': 'array', 'items': {'type': 'number'}}
            ),
        ],
        responses={
            200: TriviaSerializer,
            400: OpenApiResponse(
                description="Error en los datos enviados"
            )
        }
    )
    def put(self, request, pk):
        trivia = get_object_or_404(Trivia, pk=pk)
        serializer = TriviaSerializer(trivia, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Elimina una trivia",
        responses={
            204: OpenApiResponse(response=OpenApiTypes.OBJECT),
            404: OpenApiResponse(response=OpenApiTypes.OBJECT),
        },
    )
    def delete(self, request, pk):
        try:
            trivia = get_object_or_404(Trivia, pk=pk)
            trivia.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response({"detail": "No se encontró la trivia"}, status=status.HTTP_404_NOT_FOUND)
