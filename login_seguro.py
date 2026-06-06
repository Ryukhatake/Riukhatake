import hashlib
import re
import bcrypt
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Tuple

# Simulación de base de datos segura
# Contraseña real: "Admin@2026"
BASE_DE_DATOS = {
    "usuario@correo.com": b"$2b$12$R9h7cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jKMm6"
}

# Rastreador de intentos fallidos
intentos_fallidos = defaultdict(list)

# Configuración de seguridad
MAX_INTENTOS = 5
VENTANA_TIEMPO_MINUTOS = 15

def validar_formato_correo(correo: str) -> bool:
    """
    Valida que el correo tenga un formato válido usando regex.
    
    Args:
        correo: Correo a validar
        
    Returns:
        bool: True si el formato es válido
    """
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, correo) is not None

def verificar_rate_limiting(correo: str) -> Tuple[bool, str]:
    """
    Verifica si el usuario ha excedido el límite de intentos fallidos.
    
    Args:
        correo: Correo del usuario
        
    Returns:
        Tuple: (permitido, mensaje)
    """
    ahora = datetime.now()
    
    # Limpiar intentos antiguos
    intentos_fallidos[correo] = [
        t for t in intentos_fallidos[correo] 
        if ahora - t < timedelta(minutes=VENTANA_TIEMPO_MINUTOS)
    ]
    
    # Verificar si se excedió el límite
    if len(intentos_fallidos[correo]) >= MAX_INTENTOS:
        return False, f"Error: Demasiados intentos fallidos. Intente después de {VENTANA_TIEMPO_MINUTOS} minutos."
    
    return True, ""

def procesar_inicio_sesion(correo: str, contrasena: str) -> str:
    """
    Procesa el login con seguridad mejorada.
    
    Mejoras implementadas:
    - Validación de formato de correo
    - Rate limiting para prevenir fuerza bruta
    - Bcrypt para hash de contraseña (con salt automático)
    - Mensajes genéricos para evitar enumeración de usuarios
    - Logging de intentos fallidos
    
    Args:
        correo: Correo del usuario
        contrasena: Contraseña en texto plano
        
    Returns:
        str: Mensaje de respuesta del servidor
    """
    
    # 1. Validar formato del correo
    if not validar_formato_correo(correo):
        return "Error: Credenciales inválidas."
    
    # 2. Verificar rate limiting
    permitido, mensaje = verificar_rate_limiting(correo)
    if not permitido:
        return mensaje
    
    # 3. Verificar si el usuario existe y comparar contraseña con bcrypt
    if correo in BASE_DE_DATOS:
        try:
            # bcrypt.checkpw compara la contraseña con el hash almacenado
            if bcrypt.checkpw(contrasena.encode('utf-8'), BASE_DE_DATOS[correo]):
                # Limpiar intentos fallidos en login exitoso
                intentos_fallidos[correo].clear()
                return "¡Acceso Concedido! Autenticación exitosa."
        except Exception as e:
            print(f"[LOG] Error en verificación de bcrypt: {e}")
    
    # 4. Registrar intento fallido (sin revelar si el usuario existe o no)
    intentos_fallidos[correo].append(datetime.now())
    return "Error: Credenciales inválidas."

def generar_hash_contrasena(contrasena: str) -> str:
    """
    Genera un hash bcrypt de una contraseña.
    NOTA: Use esto solo para registrar nuevos usuarios.
    
    Args:
        contrasena: Contraseña en texto plano
        
    Returns:
        str: Hash bcrypt (puede almacenarse en la BD)
    """
    salt = bcrypt.gensalt(rounds=12)
    hash_contrasena = bcrypt.hashpw(contrasena.encode('utf-8'), salt)
    return hash_contrasena.decode('utf-8')

# --- EJECUCIÓN DEL SIMULADOR ---
if __name__ == "__main__":
    print("=== FORMULARIO DE INICIO DE SESIÓN SEGURO ===")
    print("Nota: Pruebe con 'usuario@correo.com' y 'Admin@2026' para acceso exitoso.\n")
    print("⚠️  MEJORAS DE SEGURIDAD IMPLEMENTADAS:")
    print("  • Bcrypt con salt automático (en lugar de SHA-256)")
    print("  • Rate limiting: máx 5 intentos en 15 minutos")
    print("  • Mensajes genéricos (previene enumeración de usuarios)")
    print("  • Validación de entrada robusta\n")

    # Captura de datos
    input_correo = input("Ingrese su correo electrónico: ").strip()
    input_password = input("Ingrese su contraseña: ")

    print("\n[Procesando datos de forma segura...]")
    
    # Ejecución de la lógica de control
    resultado = procesar_inicio_sesion(input_correo, input_password)
    
    print("\n=== RESPUESTA DEL SERVIDOR ===")
    print(resultado)