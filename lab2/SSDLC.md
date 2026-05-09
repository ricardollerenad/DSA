# 🔐 UML — SSDLC (Secure Software Development Life Cycle) para Login Seguro con Flask y MySQL

## 📌 Descripción

El presente documento muestra el modelado UML para un sistema de autenticación seguro desarrollado con:

- Python
- Flask
- MySQL

Aplicando principios de:

- **SSDLC (Secure Software Development Life Cycle)**

A diferencia de un SDLC tradicional, este enfoque integra mecanismos de seguridad desde las primeras etapas del desarrollo.

---

# 🎯 Objetivos de Seguridad Implementados

El sistema incorpora:

- Hashing de contraseñas
- Validación de entradas
- Protección CSRF
- Manejo seguro de sesiones
- Auditoría de accesos
- Sanitización de datos
- Registro de eventos
- Control de intentos fallidos

---

# 📖 Índice

1. Casos de Uso — SSDLC  
2. Diagrama de Secuencia — SSDLC  
3. Diagrama de Flujo — SSDLC  
4. Diagrama Entidad Relación — SSDLC  
5. Diagrama de Clases — SSDLC  
6. Diferencias entre SDLC y SSDLC  

---

# 1️⃣ Casos de Uso — SSDLC

## 📌 Descripción

Este diagrama representa las funcionalidades principales del sistema seguro de autenticación y los mecanismos de protección incorporados.

---

## 🎯 Actores

- Usuario
- Administrador
- Sistema de Seguridad

---

## 🔐 Funcionalidades de Seguridad

- Validación de entradas
- Hashing de contraseñas
- Registro de logs
- Detección de intentos fallidos
- Controles de seguridad

---

## 🧩 Código PlantUML

```plantuml
@startuml
left to right direction

actor Usuario
actor Administrador
actor SistemaSeguridad

rectangle SistemaSeguro {

    usecase "Registrarse" as UC1
    usecase "Iniciar Sesión Seguro" as UC2
    usecase "Cerrar Sesión" as UC3
    usecase "Recuperar Contraseña" as UC4

    usecase "Validar Entradas" as UC5
    usecase "Hash de Contraseña" as UC6
    usecase "Detectar Intentos Fallidos" as UC7
    usecase "Registrar Logs" as UC8
    usecase "Administrar Usuarios" as UC9
}

Usuario --> UC1
Usuario --> UC2
Usuario --> UC3
Usuario --> UC4

SistemaSeguridad --> UC5
SistemaSeguridad --> UC6
SistemaSeguridad --> UC7
SistemaSeguridad --> UC8

Administrador --> UC9

@enduml
```

---

# 🔍 Diferencias respecto al SDLC Tradicional

En SSDLC se agregan:

- Validaciones de seguridad
- Hashing de contraseñas
- Logging y auditoría
- Detección de ataques
- Controles de acceso
- Seguridad integrada desde el diseño

---

# 2️⃣ Diagrama de Secuencia — SSDLC

## 📌 Descripción

Este diagrama representa el flujo seguro de autenticación incluyendo validaciones, auditoría y verificación de credenciales cifradas.

---

## 🧩 Código PlantUML

```plantuml
@startuml

actor Usuario

participant "Flask App" as Flask
participant "Security Layer" as Security
database "MySQL" as DB

Usuario -> Flask : Login(username,password)

Flask -> Security : Validar entradas

alt Entrada inválida

    Security --> Usuario : Error validación

else Entrada válida

    Flask -> DB : Buscar usuario
    DB --> Flask : Datos usuario

    Flask -> Security : Verificar hash password

    alt Credenciales válidas

        Security -> DB : Registrar acceso
        Flask --> Usuario : Login exitoso

    else Error login

        Security -> DB : Registrar intento fallido
        Flask --> Usuario : Acceso denegado

    end

end

@enduml
```

---

# 🔍 Diferencias respecto al SDLC Tradicional

Ahora existen:

- Capa de seguridad
- Validaciones previas
- Auditoría de eventos
- Registro de intentos fallidos
- Verificación segura de contraseñas

---

# 3️⃣ Diagrama de Flujo — SSDLC

## 📌 Descripción

Representa el flujo lógico de autenticación aplicando controles de seguridad antes de conceder acceso.

---

## 🧩 Código PlantUML

```plantuml
@startuml

start

:Ingresar usuario/password;

:Validar entradas;

if (¿Entradas válidas?) then (Sí)

    :Consultar usuario;

    if (¿Usuario existe?) then (Sí)

        :Verificar hash password;

        if (¿Password válida?) then (Sí)

            :Crear sesión segura;
            :Registrar acceso;
            :Permitir acceso;

        else (No)

            :Registrar intento fallido;
            :Mostrar error;

        endif

    else (No)

        :Registrar intento sospechoso;
        :Mostrar error;

    endif

else (No)

    :Bloquear solicitud;

endif

stop

@enduml
```

---

# 4️⃣ Diagrama Entidad Relación — SSDLC

## 📌 Descripción

Este modelo representa la estructura de base de datos segura incorporando:

- Hash de contraseñas
- Logs de auditoría
- Control de intentos fallidos
- Fechas de registro

---

# 🧩 Entidades Principales

## 📦 usuarios

| Campo | Tipo |
|---|---|
| id | int |
| username | varchar |
| password_hash | varchar |
| email | varchar |
| failed_attempts | int |
| created_at | datetime |

---

## 📦 logs_seguridad

| Campo | Tipo |
|---|---|
| id | int |
| user_id | int |
| accion | varchar |
| ip | varchar |
| fecha | datetime |

---

## 🧩 Código PlantUML

```plantuml
@startuml

entity usuarios {

    * id : int
    --

    username : varchar
    password_hash : varchar
    email : varchar
    failed_attempts : int
    created_at : datetime
}

entity logs_seguridad {

    * id : int
    --

    user_id : int
    accion : varchar
    ip : varchar
    fecha : datetime
}

usuarios ||--o{ logs_seguridad

@enduml
```

---

# 🔍 Diferencias respecto al SDLC Tradicional

Se agregan:

- password_hash
- logs de auditoría
- timestamps
- control de intentos fallidos
- monitoreo de eventos

---

# 5️⃣ Diagrama de Clases — SSDLC

## 📌 Descripción

Representa la arquitectura orientada a objetos del sistema seguro incorporando una capa de seguridad especializada.

---

# 🧩 Clases Principales

## 📦 Usuario

Representa la entidad autenticada del sistema.

---

## 📦 LoginController

Gestiona:

- Login
- Logout
- Registro

---

## 📦 SecurityService

Gestiona:

- Validación de entradas
- Hashing
- Verificación de contraseñas
- Generación de CSRF
- Auditoría

---

## 📦 SecurityLog

Representa los registros de eventos de seguridad.

---

## 🧩 Código PlantUML

```plantuml
@startuml

class Usuario {

    +id : int
    +username : string
    +password_hash : string
    +email : string
    +failed_attempts : int
}

class LoginController {

    +login()
    +logout()
    +register()

}

class SecurityService {

    +validateInput()
    +hashPassword()
    +verifyPassword()
    +generateCSRF()
    +logEvent()

}

class Database {

    +connect()
    +query()

}

class SecurityLog {

    +id : int
    +accion : string
    +ip : string
    +fecha : datetime

}

LoginController --> Usuario
LoginController --> SecurityService
LoginController --> Database
SecurityService --> SecurityLog

@enduml
```

---

# 6️⃣ Diferencias entre SDLC y SSDLC

| SDLC Tradicional | SSDLC |
|---|---|
| Solo funcionalidad | Funcionalidad + seguridad |
| Password plana | Password hasheada |
| Sin validaciones | Validación estricta |
| Sin logs | Logs de auditoría |
| Sin monitoreo | Detección de ataques |
| Seguridad opcional | Seguridad integrada |
| Riesgo de SQL Injection | Prevención |
| Debug activo | Configuración segura |

---

# 📚 Tecnologías Utilizadas

- Python
- Flask
- MySQL
- PlantUML
- Git
- GitHub

---

# 🚀 Beneficios del SSDLC

Implementar SSDLC permite:

- Reducir vulnerabilidades
- Integrar seguridad desde el diseño
- Minimizar riesgos de ataques
- Mejorar la protección de credenciales
- Facilitar auditorías
- Cumplir buenas prácticas OWASP

---

# 🔐 Conclusión

El enfoque SSDLC transforma un sistema tradicional de autenticación en una aplicación mucho más segura, incorporando mecanismos de protección desde la fase de análisis y diseño.

La seguridad deja de ser un componente opcional y pasa a convertirse en parte fundamental del ciclo de vida del software.
