from django.db import models
from .constants import Dificultad
from equipo.models import Trabajador

# Create your models here.
class Pregunta(models.Model):
    dificultad = models.CharField(
        max_length=10,
        choices=Dificultad.choices,
        default=Dificultad.FACIL,
    )
    pregunta = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Alternativa(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    alternativa = models.CharField(max_length=255)
    correcta = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    alternativa = models.ForeignKey(Alternativa, on_delete=models.CASCADE)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['pregunta', 'alternativa', 'trabajador'], name='unique_respuesta')
        ]

class Trivia(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    preguntas = models.ManyToManyField(Pregunta)
    trabajadores = models.ManyToManyField(Trabajador)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre
