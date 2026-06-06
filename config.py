"""
Configuración de seguridad para el sistema de autenticación.
"""
from datetime import timedelta

# Política de contraseñas
MINIMO_CARACTERES = 8
REQUIERE_MAYUSCULA = True
REQUIERE_NUMERO = True
REQUIERE_ESPECIAL = True

# Rate limiting
MAX_INTENTOS_LOGIN = 5
VENTANA_TIEMPO_MINUTOS = 15

# Bcrypt
BCRYPT_ROUNDS = 12  # Más alto = más seguro pero más lento

# Sesiones (futuro)
DURACION_SESION_MINUTOS = 30
DURACION_SESION_RECORDAR_DIAS = 7