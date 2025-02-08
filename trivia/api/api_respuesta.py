from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from trivia.models import Respuesta
from trivia.serializers import RespuestaSerializer
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    OpenApiExample
)


class RespuestaAPI(APIView):
    
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados

    @extend_schema(
        summary="Todas las respuestas",
        responses={200: RespuestaSerializer(many=True)},
    )
    def get(self, request):
        respuestas = Respuesta.objects.all()
        serializer = RespuestaSerializer(respuestas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary="Crea una nueva respuesta",
        request=RespuestaSerializer,
        parameters=[
            OpenApiParameter(
                name="pregunta",
                description="ID de la pregunta a la que pertenece la respuesta",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="alternativa",
                description="ID de la alternativa seleccionada",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="trabajador",
                description="ID del trabajador que responde",
                required=False,
                type=int,
            ),
        ],
        responses={
            201: RespuestaSerializer,
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Error de validación",
                examples=[
                    OpenApiExample(
                        name="Ejemplo de error",
                        description="Este es un error de validación cuando el campo 'pregunta' está vacío.",
                        value={"pregunta": ["This field may not be blank."]},
                        response_only=True,  # Indica que este ejemplo es solo para respuestas
                    ),
                    OpenApiExample(
                        name="Ejemplo de error",
                        description="Este es un error de validación cuando el campo 'alternativa' está vacío.",
                        value={"alternativa": ["This field may not be blank."]},
                        response_only=True,  # Indica que este ejemplo es solo para respuestas
                    ),
                    OpenApiExample(
                        name="Ejemplo de error",
                        description="Este es un error de validación cuando el campo 'trabajador' está vacío.",
                        value={"trabajador": ["This field may not be blank."]},
                        response_only=True,  # Indica que este ejemplo es solo para respuestas
                    ),
                ],
            ),
        },
    )
    def post(self, request):
        serializer = RespuestaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RespuestaDetalleAPI(APIView):
    
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados

    @extend_schema(
        summary="Obtiene una respuesta",
        responses={
            200: RespuestaSerializer,
        },
    )
    def get(self, request, pk=None):
        if pk:
            respuesta = get_object_or_404(Respuesta, pk=pk)
            serializer = RespuestaSerializer(respuesta)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Actualiza una respuesta",
        request=RespuestaSerializer,
        parameters=[
            OpenApiParameter(
                name="pregunta",
                description="ID de la pregunta a la que pertenece la respuesta",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="alternativa",
                description="ID de la alternativa seleccionada",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="trabajador",
                description="ID del trabajador que responde",
                required=False,
                type=int,
            ),
        ],
        responses={
            200: RespuestaSerializer,
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
        respuesta = get_object_or_404(Respuesta, pk=pk)
        serializer = RespuestaSerializer(respuesta, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Elimina una respuesta",
        responses={
            204: OpenApiResponse(response=OpenApiTypes.OBJECT),
            404: OpenApiResponse(response=OpenApiTypes.OBJECT),
        },
    )
    def delete(self, request, pk):
        try:
            respuesta = get_object_or_404(Respuesta, pk=pk)
            respuesta.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:    
            return Response(status=status.HTTP_404_NOT_FOUND)
