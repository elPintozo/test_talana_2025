from django.contrib.auth import get_user_model
import os

User = get_user_model()

# Datos del superusuario desde variables de entorno
SUPERUSER_USERNAME = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
SUPERUSER_EMAIL = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
SUPERUSER_PASSWORD = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin123")

if not User.objects.filter(username=SUPERUSER_USERNAME).exists():
    print("Creando superusuario...")
    User.objects.create_superuser(SUPERUSER_USERNAME, SUPERUSER_EMAIL, SUPERUSER_PASSWORD)
    print("Superusuario creado correctamente.")
else:
    print("El superusuario ya existe.")