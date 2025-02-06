import uuid
from django.db import models
from django.contrib.auth.models import User

class Trabajador(models.Model):
    identificador = models.CharField(max_length=6, unique=True, editable=False, default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    nombre = models.CharField(max_length=255)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Si no tiene identificador, se le asigna uno
        if not self.identificador:
            self.identificador = str(uuid.uuid4().int)[:6]

        # crear y asociar un usuario
        if not self.user:
            self.user = User.objects.create_user(
                username=f"{self.nombre}_{self.identificador[:4]}",
                email=self.email,
                password='Talana2025'
            )
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.nombre} {self.user.last_name}'
    