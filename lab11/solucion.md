# Laboratorio 11: Gestión Segura de Sesiones con Flask y Flask-Login

## Objetivo

Implementar un sistema de autenticación seguro utilizando **Flask**, **Flask-Login** y **SQLAlchemy**, aplicando buenas prácticas de ciberseguridad para la gestión de sesiones de usuario.

Al finalizar este laboratorio el estudiante será capaz de:

- Configurar un entorno virtual de desarrollo.
- Implementar autenticación segura utilizando Flask-Login.
- Almacenar contraseñas mediante funciones hash.
- Proteger rutas mediante sesiones autenticadas.
- Implementar cierre seguro de sesión.
- Integrar una base de datos MySQL mediante SQLAlchemy.
- Validar el funcionamiento del sistema siguiendo buenas prácticas de seguridad (OWASP).

---

# Actividad 1. Preparación del entorno de desarrollo

En esta actividad se creará el entorno de trabajo aislado para el proyecto y se instalarán todas las dependencias necesarias.

## 1. Crear el proyecto

```bash
mkdir laboratorio11_seguridad
cd laboratorio11_seguridad
```

---

## 2. Crear el entorno virtual

> Requiere Python 3.10 o superior.

```bash
python -m venv venv
```

Activar el entorno virtual.

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

---

## 3. Instalar las dependencias

```bash
pip install Flask
pip install flask-login
pip install flask-sqlalchemy
pip install pymysql
pip install Werkzeug
```

O bien instalar todo en un solo comando.

```bash
pip install Flask flask-login flask-sqlalchemy pymysql Werkzeug
```

---

## 4. Generar el archivo de dependencias

```bash
pip freeze > requirements.txt
```

---

# Actividad 2. Configuración de la aplicación Flask

En esta actividad se configurará la aplicación junto con Flask-Login y SQLAlchemy.

## Crear el archivo `app.py`

```python
import os

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# ==================================================
# CONFIGURACIÓN DE SEGURIDAD
# ==================================================

app.config["SECRET_KEY"] = "mi_clave_secreta_super_segura_12345"

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:password@localhost:3306/laboratorio11_db"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ==================================================
# CONFIGURACIÓN DE FLASK LOGIN
# ==================================================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"

login_manager.login_message_category = "warning"
```

> **Importante**
>
> En un entorno de producción **nunca** se debe almacenar la `SECRET_KEY` directamente en el código fuente. Se recomienda utilizar variables de entorno.

---

# Actividad 3. Modelo de usuario

Crear el modelo que será utilizado por Flask-Login y SQLAlchemy.

```python
class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)
```

---

## Configurar el `user_loader`

```python
@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))
```

El método `user_loader` permite recuperar el usuario autenticado a partir del identificador almacenado en la sesión.

---

# Actividad 4. Implementación del inicio de sesión

Agregar la ruta encargada del proceso de autenticación.

```python
@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        username = request.form.get("username")

        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):

            login_user(user)

            return redirect(url_for("dashboard"))

        flash(
            "Credenciales inválidas. Intente nuevamente.",
            "danger"
        )

    return render_template("login.html")
```

### Buenas prácticas implementadas

- Uso de `check_password_hash()`.
- Contraseñas almacenadas mediante hash.
- Mensaje genérico para evitar enumeración de usuarios.
- No se almacena la contraseña en texto plano.

---

# Actividad 5. Protección de rutas

Las rutas privadas deberán utilizar el decorador `@login_required`.

```python
@app.route("/dashboard")
@login_required
def dashboard():

    return render_template("dashboard.html")
```

Cuando un usuario no autenticado intente acceder al Dashboard será redirigido automáticamente al Login.

---

# Actividad 6. Cierre seguro de sesión

Agregar la ruta para cerrar la sesión del usuario.

```python
@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Has cerrado sesión de forma segura.",
        "success"
    )

    return redirect(url_for("login"))
```

---

# Actividad 7. Crear las tablas automáticamente

Al iniciar la aplicación crear las tablas si no existen.

```python
with app.app_context():

    db.create_all()

if __name__ == "__main__":

    app.run(debug=True)
```

---

# Registrar un usuario administrador

La primera vez que se ejecute el sistema la tabla estará vacía.

Crear un archivo llamado `crear_usuario.py`.

```python
from app import app, db, User

from werkzeug.security import generate_password_hash

with app.app_context():

    usuario = User(
        username="admin",
        password_hash=generate_password_hash("password123")
    )

    db.session.add(usuario)

    db.session.commit()

    print("Usuario creado correctamente.")
```

Ejecutar:

```bash
python crear_usuario.py
```

---

# Actividad 8. Crear las vistas HTML

## Estructura

```text
templates/
│
├── login.html
└── dashboard.html
```

---

## login.html

```html
<!DOCTYPE html>

<html lang="es">

<head>

    <meta charset="UTF-8">

    <title>Inicio de Sesión</title>

</head>

<body>

<h2>Control de Acceso</h2>

{% with messages = get_flashed_messages(with_categories=true) %}
{% if messages %}
{% for category, message in messages %}

<p style="color:red;">
    [{{ category.upper() }}] {{ message }}
</p>

{% endfor %}
{% endif %}
{% endwith %}

<form method="POST">

<label>Usuario</label>

<input
type="text"
name="username"
required
autocomplete="off">

<br><br>

<label>Contraseña</label>

<input
type="password"
name="password"
required>

<br><br>

<button type="submit">

Ingresar

</button>

</form>

</body>

</html>
```

---

## dashboard.html

```html
<!DOCTYPE html>

<html lang="es">

<head>

<meta charset="UTF-8">

<title>Dashboard</title>

</head>

<body>

<h1>

Bienvenido {{ current_user.username }}

</h1>

<p>

Has iniciado sesión correctamente.

</p>

<a href="{{ url_for('logout') }}">

Cerrar sesión

</a>

</body>

</html>
```

---

# Actividad 9. Validación del sistema

## Paso 1

Ejecutar la aplicación.

```bash
python app.py
```

---

## Paso 2

Intentar acceder directamente a:

```
http://127.0.0.1:5000/dashboard
```

**Resultado esperado**

El sistema deberá redirigir automáticamente al Login.

---

## Paso 3

Ingresar las credenciales.

| Usuario | Contraseña |
|----------|------------|
| admin | password123 |

**Resultado esperado**

El usuario accederá correctamente al Dashboard.

---

## Paso 4

Cerrar sesión.

**Resultado esperado**

El usuario será redirigido nuevamente al Login.

Si intenta volver al Dashboard sin autenticarse, el sistema deberá bloquear el acceso.

---

# Base de datos

## Crear la base de datos

```sql
CREATE DATABASE IF NOT EXISTS laboratorio11_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE laboratorio11_db;
```

---

## Crear la tabla

```sql
CREATE TABLE IF NOT EXISTS users(

    id INT AUTO_INCREMENT PRIMARY KEY,

    username VARCHAR(50) UNIQUE NOT NULL,

    password_hash VARCHAR(255) NOT NULL

);
```

---

## Insertar un usuario administrador

```sql
INSERT INTO users(username,password_hash)

VALUES(

'admin',

'pbkdf2:sha256:600000$uG7xR8Wz8mJ9$4e3f42c674bb96da60431bdf7f3efc29184ba5dfcd7f3e8b0a9442a6c0b9a9d7'

)

ON DUPLICATE KEY UPDATE username=username;
```

---

# Estructura del proyecto

```text
laboratorio11_seguridad/
│
├── templates/
│   ├── login.html
│   └── dashboard.html
│
├── venv/
│
├── app.py
│
├── requirements.txt
│
├── .gitignore
│
└── crear_usuario.py
```

---

# Archivo `.gitignore`

```gitignore
venv/

__pycache__/

*.pyc

.env

.vscode/

.idea/

instance/

*.db
```

---

# Consideraciones de seguridad

Durante el desarrollo se aplicaron las siguientes buenas prácticas:

- Las contraseñas nunca se almacenan en texto plano.
- Se utiliza `generate_password_hash()` para generar hashes seguros.
- La autenticación utiliza `check_password_hash()`.
- Las rutas privadas están protegidas mediante `@login_required`.
- Se implementa un cierre seguro de sesión mediante `logout_user()`.
- Se utiliza una `SECRET_KEY` para firmar las cookies de sesión.
- En producción la `SECRET_KEY` y las credenciales de la base de datos deben almacenarse en variables de entorno.
- Se evita la enumeración de usuarios mostrando mensajes de error genéricos.

---

# Conclusiones

Al finalizar este laboratorio se implementó un sistema de autenticación basado en Flask siguiendo recomendaciones de seguridad alineadas con las buenas prácticas de OWASP. El sistema incorpora autenticación mediante sesiones, almacenamiento seguro de contraseñas utilizando funciones hash, protección de rutas privadas, cierre seguro de sesión e integración con una base de datos MySQL mediante SQLAlchemy.
