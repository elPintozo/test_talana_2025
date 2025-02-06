from django.db import models

class Dificultad(models.TextChoices):
    FACIL = 'facil', 'Fácil'
    MEDIO = 'medio', 'Medio'
    DIFICIL = 'dificil', 'Difícil'