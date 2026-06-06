# 🔒 Sistema de Autenticación Seguro

Sistema de login mejorado con mejores prácticas de seguridad implementadas.

## ✅ Mejoras de Seguridad Implementadas

### 1. **Bcrypt en lugar de SHA-256**
```python
# ❌ Antes (inseguro)
hash_ingresado = hashlib.sha256(contrasena_bytes).hexdigest()

# ✅ Ahora (seguro)
bcrypt.checkpw(contrasena.encode('utf-8'), hash_almacenado)
```
- SHA-256 es demasiado rápido para fuerza bruta
- Bcrypt incluye salt automático y es adaptable

### 2. **Rate Limiting**
- Máximo 5 intentos fallidos por usuario
- Ventana de tiempo: 15 minutos
- Previene ataques de fuerza bruta

### 3. **Prevención de Enumeración de Usuarios**
```python
# ❌ Antes (revela usuarios)
"Error: El usuario no está registrado."
"Error: Contraseña incorrecta."

# ✅ Ahora (genérico)
"Error: Credenciales inválidas."
```

### 4. **Validación Robusta**
- Validación de formato de correo con regex
- Manejo de excepciones
- Entrada sanitizada

## 🚀 Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt
```

## 📖 Uso

```python
from login_seguro import procesar_inicio_sesion

resultado = procesar_inicio_sesion("usuario@correo.com", "Admin@2026")
print(resultado)  # "¡Acceso Concedido! Autenticación exitosa."
```

## 🧪 Ejecutar Tests

```bash
python test_seguridad.py
```

## 🔑 Generar Hash para Nuevos Usuarios

```python
from login_seguro import generar_hash_contrasena

# Al registrar un nuevo usuario:
contrasena = "MiContrasena@123"
hash_bcrypt = generar_hash_contrasena(contrasena)
print(hash_bcrypt)  # $2b$12$...
# Almacenar en la BD
```

## 📊 Comparación de Seguridad

| Aspecto | Antes | Ahora |
|---------|-------|-------|
| **Algoritmo Hash** | SHA-256 | Bcrypt (rounds=12) |
| **Salt** | No | Sí (automático) |
| **Rate Limiting** | No | Sí (5 intentos/15 min) |
| **Enumeración Usuarios** | Vulnerable | Protegido |
| **Tiempo Hash** | ~1ms | ~200ms |

## ⚠️ Consideraciones Futuras

- [ ] Implementar 2FA (Two-Factor Authentication)
- [ ] Agregar HTTPS/TLS
- [ ] Logging y monitoreo de intentos
- [ ] Bloqueo temporal de cuenta
- [ ] Recuperación de contraseña segura
- [ ] Tokens JWT para sesiones

## 📚 Referencias

- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [Bcrypt Documentation](https://github.com/pyca/bcrypt)
- [CWE-521: Weak Password Requirements](https://cwe.mitre.org/data/definitions/521.html)

## 📄 Licencia

MIT