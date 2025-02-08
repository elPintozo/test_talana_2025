from django.urls import path
from trivia.api.api_pregunta import PreguntaAPI, PreguntaDetalleAPI
from trivia.api.api_alternativa import AlternativaAPI, AlternativaDetalleAPI, AlternativasPorPreguntaAPI
from trivia.api.api_respuesta import RespuestaAPI, RespuestaDetalleAPI
from trivia.api.api_trivia import TriviaAPI, TriviaDetalleAPI

urlpatterns = [
    path('pregunta/', PreguntaAPI.as_view(), name='pregunta-listar-crear'),  # Listar y crear preguntas
    path('pregunta/<int:pk>', PreguntaDetalleAPI.as_view(), name='pregunta-actualizar-detalle'),  # actualizar, eliminar y ver preguntas

    path('alternativa/', AlternativaAPI.as_view(), name='alternativa-crear-listar'),  # Crear y listar alternativas
    path('alternativa/<int:pk>', AlternativaDetalleAPI.as_view(), name='alternativa-actualizar-detalle'),  # actualizar, eliminar y ver alternativas
    path('pregunta/<int:pregunta_id>/alternativas', AlternativasPorPreguntaAPI.as_view(), name='alternativas-por-pregunta'),  # Obtener las alternativas de una pregunta

    path('respuesta/', RespuestaAPI.as_view(), name='respuesta-crear-listar'),  # Crear y listar respuestas
    path('respuesta/<int:pk>', RespuestaDetalleAPI.as_view(), name='respuesta-actualizar-detalle'),  # actualizar, eliminar y ver respuestas

    path('trivia/', TriviaAPI.as_view(), name='trivia-crear-listar'),  # Crear y listar trivias
    path('trivia/<int:pk>', TriviaDetalleAPI.as_view(), name='trivia-actualizar-detalle'),  # actualizar trivias
]
