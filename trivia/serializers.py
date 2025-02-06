from rest_framework import serializers
from .models import Pregunta, Alternativa, Respuesta, Trivia


class PreguntaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregunta
        fields = '__all__'


class AlternativaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alternativa
        fields = '__all__'


class RespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuesta
        fields = '__all__'


class TriviaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trivia
        fields = '__all__'