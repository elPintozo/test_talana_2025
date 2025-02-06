from django.urls import path
from trivia.api.api_pregunta import PreguntaAPI
from trivia.api.api_alternativa import AlternativaAPI, AlternativasPorPreguntaAPI
from trivia.api.api_respuesta import RespuestaAPI
from trivia.api.api_trivia import TriviaAPI

urlpatterns = [
    path('pregunta/', PreguntaAPI.as_view(), name='pregunta-crear-listar'),  # crear y listar preguntas
    path('pregunta/<int:pk>', PreguntaAPI.as_view(), name='pregunta-actualizar'),  # actualizar preguntas

    path('alternativa/', AlternativaAPI.as_view(), name='alternativa-crear-listar'),  # Crear y listar alternativas
    path('alternativa/<int:pk>', AlternativaAPI.as_view(), name='alternativa-actualizar'),  # actualizar alternativas
    path('pregunta/<int:pregunta_id>/alternativas', AlternativasPorPreguntaAPI.as_view(), name='alternativas-por-pregunta'),  # Obtener las alternativas de una pregunta

    path('respuesta/', RespuestaAPI.as_view(), name='respuesta-crear-listar'),  # Crear y listar respuestas
    path('respuesta/<int:pk>', RespuestaAPI.as_view(), name='respuesta-actualizar'),  # actualizar respuestas

    path('trivia/', TriviaAPI.as_view(), name='trivia-crear-listar'),  # Crear y listar trivias
    path('trivia/<int:pk>', TriviaAPI.as_view(), name='trivia-actualizar'),  # actualizar trivias
]
