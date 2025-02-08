from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from trivia.models import Pregunta, Alternativa
from trivia.serializers import AlternativaSerializer
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    OpenApiExample
)


class AlternativaAPI(APIView):

    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados
    
    @extend_schema(
        summary="Todas las alternativas",
        responses={200: AlternativaSerializer(many=True)},
    )
    def get(self, request):
        alternativas = Alternativa.objects.all()
        serializer = AlternativaSerializer(alternativas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Crea una nueva alternativa",
        request=AlternativaSerializer,
        parameters=[
            OpenApiParameter(
                name="pregunta",
                description="Pk de la pregunta",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="alternativa",
                description="Texto de la alternativa",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="correcta",
                description="Indica si la alternativa es correcta",
                required=False,
                type=bool,
            ),
        ],
        responses={
            201: AlternativaSerializer,
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Error de validación",
                examples=[
                    OpenApiExample(
                        name="Ejemplo de error",
                        description="Este es un error de validación cuando el campo 'alternativa' está vacío.",
                        value={"alternativa": ["This field may not be blank."]},
                        response_only=True,  # Indica que este ejemplo es solo para respuestas
                    )
                ],
            ),
        },
    )
    def post(self, request):
        serializer = AlternativaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlternativaDetalleAPI(APIView):

    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados

    @extend_schema(
        summary="Obtiene los detalles de una alternativa",
        responses={
            200: AlternativaSerializer,
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Error de validación",
                examples=[
                    OpenApiExample(
                        name="Ejemplo de error",
                        description="Este es un error de validación cuando el campo 'pk' está vacío.",
                        value={"pk": ["This field may not be blank."]},
                        response_only=True,  # Indica que este ejemplo es solo para respuestas
                    )
                ],
            ),
        },
    )
    def get(self, request, pk=None):
        if pk:
            alternativa = get_object_or_404(Alternativa, pk=pk)
            serializer = AlternativaSerializer(alternativa)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Actualiza una alternativa",
        request=AlternativaSerializer,
        parameters=[
            OpenApiParameter(
                name="pregunta",
                description="Pk de la pregunta",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="alternativa",
                description="Texto de la alternativa",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="correcta",
                description="Indica si la alternativa es correcta",
                required=False,
                type=bool,
            ),
        ],
        responses={
            200: AlternativaSerializer,
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Error de validación",
                examples=[
                    OpenApiExample(
                        name="Ejemplo de error",
                        description="Este es un error de validación cuando el campo 'alternativa' está vacío.",
                        value={"alternativa": ["This field is required."]},
                        response_only=True,  # Indica que este ejemplo es solo para respuestas
                    )
                ],
            ),
        },
    )
    def put(self, request, pk):
        alternativa = get_object_or_404(Alternativa, pk=pk)
        serializer = AlternativaSerializer(alternativa, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Elimina una alternativa",
        responses={
            204: OpenApiResponse(response=OpenApiTypes.OBJECT),
            404: OpenApiResponse(response=OpenApiTypes.OBJECT),
        },
    )
    def delete(self, request, pk):
        try:
            alternativa = get_object_or_404(Alternativa, pk=pk)
            alternativa.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({}, status=status.HTTP_204_NO_CONTENT)


class AlternativasPorPreguntaAPI(APIView):

    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados

    @extend_schema(
        summary="Obtiene las alternativas de una pregunta",
        responses={
            200: AlternativaSerializer(many=True),
            404: OpenApiResponse(response=OpenApiTypes.OBJECT),
        },
    )
    def get(self, request, pregunta_id):
        try:
            pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
            alternativas = Alternativa.objects.filter(pregunta=pregunta)
            serializer = AlternativaSerializer(alternativas, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
