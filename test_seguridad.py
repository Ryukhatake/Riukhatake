"""
Tests para validar las mejoras de seguridad en el sistema de login.
"""
import unittest
from datetime import datetime, timedelta
from login_seguro import (
    procesar_inicio_sesion,
    validar_formato_correo,
    generar_hash_contrasena,
    intentos_fallidos
)

class TestSeguridad(unittest.TestCase):
    
    def setUp(self):
        """Limpiar estado antes de cada test."""
        intentos_fallidos.clear()
    
    def test_login_correcto(self):
        """Login con credenciales correctas."""
        resultado = procesar_inicio_sesion("usuario@correo.com", "Admin@2026")
        self.assertIn("Acceso Concedido", resultado)
    
    def test_contrasena_incorrecta(self):
        """Login con contraseña incorrecta."""
        resultado = procesar_inicio_sesion("usuario@correo.com", "WrongPassword123")
        self.assertIn("Credenciales inválidas", resultado)
    
    def test_correo_invalido(self):
        """Validación de formato de correo."""
        self.assertFalse(validar_formato_correo("correo_invalido"))
        self.assertFalse(validar_formato_correo("@correo.com"))
        self.assertTrue(validar_formato_correo("usuario@correo.com"))
    
    def test_rate_limiting(self):
        """Verificar que rate limiting funciona."""
        # Hacer 5 intentos fallidos
        for i in range(5):
            procesar_inicio_sesion("usuario@correo.com", "contraseña_falsa")
        
        # El 6to intento debe ser bloqueado
        resultado = procesar_inicio_sesion("usuario@correo.com", "Admin@2026")
        self.assertIn("Demasiados intentos", resultado)
    
    def test_sin_enumeracion_usuarios(self):
        """Verificar que no se revela si un usuario existe."""
        resultado_usuario_inexistente = procesar_inicio_sesion("noexiste@correo.com", "cualquier_pwd")
        resultado_contrasena_falsa = procesar_inicio_sesion("usuario@correo.com", "contraseña_falsa")
        
        # Ambos deben tener el mismo mensaje
        self.assertEqual(resultado_usuario_inexistente, resultado_contrasena_falsa)
    
    def test_generador_hash_bcrypt(self):
        """Verificar que generar_hash_contrasena funciona."""
        hash1 = generar_hash_contrasena("Test@123")
        hash2 = generar_hash_contrasena("Test@123")
        
        # Los hashes deben ser diferentes (salt diferente)
        self.assertNotEqual(hash1, hash2)
        print(f"Hash 1: {hash1}")
        print(f"Hash 2: {hash2}")

if __name__ == '__main__':
    unittest.main()