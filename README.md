# 🔐 Curso: Diseño Seguro de Aplicaciones Web con Flask + MySQL

## 📌 Descripción general

Este repositorio forma parte de un **curso práctico de desarrollo seguro de aplicaciones web**, donde aprenderás a construir un sistema de autenticación (login y registro) utilizando:

- Python
- Flask
- MySQL (XAMPP)
- Entornos virtuales
- Buenas prácticas de seguridad
- SSDLC (Secure Software Development Life Cycle)

---

## 🎯 Objetivo del curso

El objetivo principal es que el estudiante sea capaz de:

- Desarrollar aplicaciones web con Flask
- Integrar bases de datos MySQL
- Implementar un sistema de login seguro
- Aplicar principios de seguridad desde el diseño
- Comprender la diferencia entre SDLC y SSDLC
- Modelar sistemas con diagramas UML

---

## 🧠 Contenidos del curso

### 🟢 1. Fundamentos de desarrollo web seguro

- Buenas prácticas de seguridad
- Validación de entradas
- Protección de credenciales
- Separación de configuraciones
- Principios OWASP

---

### 🟡 2. SDLC (Software Development Life Cycle)

Incluye:

- Modelado UML tradicional
- Diseño de login básico
- Arquitectura sin enfoque de seguridad
- Riesgos comunes en aplicaciones web

📌 Diagramas incluidos:
- Casos de uso
- Secuencia
- Flujo
- ER
- Clases

---

### 🔴 3. SSDLC (Secure Software Development Life Cycle)

Incluye:

- Diseño seguro desde el inicio
- Hashing de contraseñas
- Validación de entradas
- Auditoría de eventos
- Control de intentos fallidos
- Protección CSRF (conceptual)

📌 Diagramas incluidos:
- Casos de uso seguro
- Secuencia con capa de seguridad
- Flujo seguro
- ER con logs
- Arquitectura de clases seguras

---

### 🟣 4. Implementación práctica del sistema

Desarrollo completo de:

- Registro de usuarios
- Login seguro
- Sesión de usuario
- Logout
- Conexión a MySQL
- Uso de `.env`

---

## 🛠️ Tecnologías utilizadas

- Python 3.12+
- Flask
- MySQL (XAMPP)
- Werkzeug (hashing)
- python-dotenv
- Git / GitHub
- PlantUML

---

## 📁 Estructura del proyecto

```
flask_secure_login/
│
├── app.py
├── .env
├── requirements.txt
├── venv/
│
└── templates/
    ├── login.html
    └── register.html
```

---

## 🔐 Características del sistema

- 🔑 Autenticación de usuarios
- 🔒 Contraseñas con hashing seguro
- 🧾 Registro de usuarios en MySQL
- 🚫 Validación de entradas
- 🔁 Manejo de sesiones
- ⚠️ Protección contra accesos inválidos
- 📊 Base para auditoría de seguridad

---

## ⚖️ Comparación SDLC vs SSDLC

| SDLC Tradicional | SSDLC (Seguro) |
|---|---|
| Solo funcionalidad | Funcionalidad + seguridad |
| Password en texto plano | Password hasheada |
| Sin validaciones | Validación estricta |
| Sin logs | Auditoría y logs |
| Sin control de ataques | Detección de intentos fallidos |
| Riesgo SQL Injection | Prevención desde diseño |

---

## 📊 Modelado UML

En este curso se trabaja con:

### SDLC tradicional:
- Casos de uso básicos
- Flujo simple de login
- Base de datos sin seguridad
- Arquitectura simple

### SSDLC:
- Capa de seguridad
- Logs de auditoría
- Hashing de contraseñas
- Flujo seguro de autenticación
- Control de ataques

---

## 🚀 Cómo ejecutar el proyecto

### 1. Crear entorno virtual

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 2. Instalar dependencias

```bash
pip install flask flask-mysqldb werkzeug python-dotenv
```

---

### 3. Ejecutar MySQL en XAMPP

- Iniciar Apache
- Iniciar MySQL
- Crear base de datos desde phpMyAdmin

---

### 4. Ejecutar aplicación

```bash
python app.py
```

---

### 5. Acceder en navegador

```
http://127.0.0.1:5000
```

---

## 🔮 Mejoras futuras

Este proyecto puede evolucionar hacia:

- JWT Authentication
- Flask-WTF (CSRF Protection)
- 2FA (Two Factor Authentication)
- CAPTCHA
- Roles y permisos
- API REST segura
- SQLAlchemy ORM
- Dockerización
- Deploy en VPS (Linux + Nginx)
- Cumplimiento OWASP Top 10

---

## 📚 Conclusión del curso

Este curso permite comprender cómo un sistema de autenticación puede evolucionar desde un diseño básico (SDLC) hasta un sistema robusto y seguro (SSDLC), aplicando buenas prácticas reales de la industria del software.

El estudiante no solo programa, sino que **diseña pensando en seguridad desde el inicio**.
```
