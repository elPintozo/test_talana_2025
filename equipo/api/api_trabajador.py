from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from equipo.models import Trabajador
from equipo.serializers import TrabajadorSerializer
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    OpenApiExample
)


class TrabajadorAPI(APIView):

    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados
    
    @extend_schema(
        summary="Todos los trabajadores",
        responses={200: TrabajadorSerializer(many=True)},
    )
    def get(self, request):
        trabajadores = Trabajador.objects.filter(user__is_superuser=False)
        serializer = TrabajadorSerializer(trabajadores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary="Crea un nuevo trabajador",
        request=TrabajadorSerializer,
        parameters=[
            OpenApiParameter(
                name="nombre",
                description="Nombre del trabajador",
            ),
            OpenApiParameter(
                name="email",
                description="Correo electrónico del trabajador",
            ),
        ],
        responses={
            201: TrabajadorSerializer,
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
                        description="Este es un error de validación cuando el campo 'email' está vacío.",
                        value={"email": ["This field is required."]},
                        response_only=True,  # Indica que este ejemplo es solo para respuestas
                    )
                ],
            ),
        },
    )
    def post(self, request):
        serializer = TrabajadorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrabajadorDetalleAPI(APIView):

    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados

    @extend_schema(
        summary="Obtener el detalle de trabajador",
        responses={
            200: TrabajadorSerializer,
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Error",
                examples=[
                    OpenApiExample(
                        name="Ejemplo de error",
                        description="Este es un error cuando no se envía el ID del trabajador.",
                        value={"detail": "Bad request."},
                        response_only=True,  # Indica que este ejemplo es solo para respuestas
                    ),
                ],
            ),
        },
    )
    def get(self, request, pk=None):
        if pk:
            trabajador = get_object_or_404(Trabajador, pk=pk, user__is_superuser=False)
            serializer = TrabajadorSerializer(trabajador)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Actualizar el detalle de trabajador",
        request=TrabajadorSerializer,
        parameters=[
            OpenApiParameter(
                name="nombre",
                description="Nombre del trabajador",
            ),
            OpenApiParameter(
                name="email",
                description="Correo electrónico del trabajador",
            ),
        ],
        responses={
            200: TrabajadorSerializer,
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
                        description="Este es un error de validación cuando el campo 'email' está vacío.",
                        value={"email": ["This field is required."]},
                        response_only=True,  # Indica que este ejemplo es solo para respuestas
                    )
                ],
            ),
        },
    )
    def put(self, request, pk):
        trabajador = get_object_or_404(Trabajador, pk=pk)
        serializer = TrabajadorSerializer(trabajador, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Eliminar un trabajador",
        responses={
            204: OpenApiResponse(response=OpenApiTypes.OBJECT),
            404: OpenApiResponse(response=OpenApiTypes.OBJECT),
        },
    )
    def delete(self, request, pk):
        try:
            trabajador = get_object_or_404(Trabajador, pk=pk)
            trabajador.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class TrabajadorAdministradorAPI(APIView):

    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados
    
    @extend_schema(
        summary="Todos los administradores",
        responses={200: TrabajadorSerializer(many=True)},
    )
    def get(self, request):
        trabajadores = Trabajador.objects.filter(user__is_superuser=True)
        serializer = TrabajadorSerializer(trabajadores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TrabajadorAdministradorDetalleAPI(APIView):

    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados

    @extend_schema(
        summary="Obtener el detalle de un administrador",
        responses={
            200: TrabajadorSerializer,
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Error",
                examples=[
                    OpenApiExample(
                        name="Ejemplo de error",
                        description="Este es un error cuando no se envía el ID del administrador.",
                        value={"detail": "Bad request."},
                        response_only=True,  # Indica que este ejemplo es solo para respuestas
                    ),
                ],
            ),
        },
    )
    def get(self, request, pk=None):
        if pk:
            trabajador = get_object_or_404(Trabajador, pk=pk, user__is_superuser=True)
            serializer = TrabajadorSerializer(trabajador)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Crear un nuevo administrador",
        request=TrabajadorSerializer,
        parameters=[
            OpenApiParameter(
                name="nombre",
                description="Nombre del administrador",
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="email",
                description="Correo electrónico del administrador",
                type=OpenApiTypes.STR,
            ),
        ],
        responses={
            200: TrabajadorSerializer,
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
                        description="Este es un error de validación cuando el campo 'email' está vacío.",
                        value={"email": ["This field is required."]},
                        response_only=True,  # Indica que este ejemplo es solo para respuestas
                    )
                ],
            ),
        },
    )
    def post(self, request):
        serializer = TrabajadorSerializer(data=request.data)
        if serializer.is_valid():

            nuevo_adminitrador = serializer.save()
            nuevo_adminitrador.user.is_superuser = True
            nuevo_adminitrador.user.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
