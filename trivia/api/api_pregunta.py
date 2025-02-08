from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from trivia.models import Pregunta
from trivia.constants import Dificultad
from trivia.serializers import PreguntaSerializer
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    OpenApiExample
)

class PreguntaAPI(APIView):
    
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados

    @extend_schema(
        summary="Todas las preguntas",
        responses={200: PreguntaSerializer(many=True)},
    )
    def get(self, request):
        preguntas = Pregunta.objects.all()
        serializer = PreguntaSerializer(preguntas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Crea una nueva pregunta",
        request=PreguntaSerializer,
        parameters=[
            OpenApiParameter(
                name="dificultad",
                description="Dificultad de la pregunta",
                enum=[ x[0] for x in Dificultad.choices ]
            ),
            OpenApiParameter(
                name="pregunta",
                description="Texto de la pregunta",
            ),
        ],
        responses={
            201: PreguntaSerializer,
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Error de validación",
                examples=[
                    OpenApiExample(
                        name="Ejemplo de error",
                        description="Este es un error de validación cuando el campo 'pregunta' está vacío.",
                        value={"pregunta": ["This field is required."]},
                        response_only=True,  # Indica que este ejemplo es solo para respuestas
                    )
                ],
            ),
        },
    )
    def post(self, request):
        serializer = PreguntaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PreguntaDetalleAPI(APIView):
    
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados
    
    @extend_schema(
        summary="Obtiene el detalle de una pregunta",
        responses={200: PreguntaSerializer(many=True)},
    )
    def get(self, request, pk=None):
        if pk:
            pregunta = get_object_or_404(Pregunta, pk=pk)
            serializer = PreguntaSerializer(pregunta)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Actualiza una pregunta",
        request=PreguntaSerializer,
        responses={
            200: PreguntaSerializer,
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Error de validación",
                examples=[
                    OpenApiExample(
                        name="Ejemplo de error",
                        description="Este es un error de validación cuando el campo 'pregunta' está vacío.",
                        value={"pregunta": ["This field may not be blank."]},
                        response_only=True,  # Indica que este ejemplo es solo para respuestas
                    )
                ],
            ),
        },
    )
    def put(self, request, pk):
        pregunta = get_object_or_404(Pregunta, pk=pk)
        serializer = PreguntaSerializer(pregunta, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Elimina una pregunta",
        responses={
            204: OpenApiResponse(response=OpenApiTypes.OBJECT),
            404: OpenApiResponse(response=OpenApiTypes.OBJECT),
        },
    )
    def delete(self, request, pk):
        try:
            pregunta = get_object_or_404(Pregunta, pk=pk)
            pregunta.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
