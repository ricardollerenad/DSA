# 🔐 Flask Secure Login - Laboratorio Completo

## REQUISITOS
Instalar: Python 3.12+, XAMPP, VS Code, Git

## CREAR PROYECTO
```bash
mkdir flask_secure_login
cd flask_secure_login
```

## CREAR ENTORNO VIRTUAL
```bash
python -m venv venv
```

## ACTIVAR ENTORNO (Windows)
```bash
venv\Scripts\activate
```

## INSTALAR DEPENDENCIAS
```bash
pip install flask flask-mysqldb werkzeug python-dotenv
```

## GENERAR REQUIREMENTS
```bash
pip freeze > requirements.txt
```

## BASE DE DATOS (XAMPP)
Iniciar Apache y MySQL y abrir:
http://localhost/phpmyadmin

SQL:
```sql
CREATE DATABASE secure_login;
USE secure_login;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100),
    password_hash VARCHAR(255) NOT NULL,
    failed_attempts INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## ESTRUCTURA
```
flask_secure_login/
├── venv/
├── app.py
├── .env
├── requirements.txt
└── templates/
    ├── login.html
    ├── home.html
    └── register.html
```

## ARCHIVO .env
```
SECRET_KEY=super_secret_key_2026
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DB=secure_login
```

## APP.PY
```python
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "clave_super_segura_2026"


# -----------------------
# LOGIN
# -----------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # 🔐 SIMULACIÓN DE USUARIO (luego lo conectas a MySQL)
        if username == "admin" and password == "1234":
            session["user"] = username
            flash("Bienvenido al sistema", "success")
            return redirect(url_for("home"))
        else:
            flash("Usuario o contraseña incorrectos", "danger")

    return render_template("login.html")


# -----------------------
# REGISTRO (simulado)
# -----------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        flash("Usuario registrado correctamente (simulado)", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# -----------------------
# HOME (BIENVENIDA)
# -----------------------
@app.route("/home")
def home():
    if "user" not in session:
        flash("Debes iniciar sesión primero", "warning")
        return redirect(url_for("login"))

    return render_template("home.html", user=session["user"])


# -----------------------
# LOGOUT
# -----------------------
@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente", "info")
    return redirect(url_for("login"))


# -----------------------
# REDIRECCIÓN INICIAL
# -----------------------
@app.route("/")
def index():
    return redirect(url_for("login"))


# -----------------------
# MAIN
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)
```

## LOGIN.HTML
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Login</title>

    <!-- Bootstrap 5 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body class="bg-light">

<div class="container d-flex justify-content-center align-items-center vh-100">

    <div class="card shadow-lg p-4" style="min-width: 350px; max-width: 400px; width: 100%; border-radius: 12px;">

        <div class="text-center mb-4">
            <h3 class="fw-bold">Login Seguro</h3>
            <p class="text-muted">Accede a tu sistema</p>
        </div>

        <form method="POST">

            <div class="mb-3">
                <label class="form-label">Usuario</label>
                <input type="text" name="username" class="form-control" placeholder="Ingresa tu usuario" required>
            </div>

            <div class="mb-3">
                <label class="form-label">Contraseña</label>
                <input type="password" name="password" class="form-control" placeholder="Ingresa tu contraseña" required>
            </div>

            <div class="d-grid mb-3">
                <button type="submit" class="btn btn-primary btn-lg">
                    Ingresar
                </button>
            </div>

        </form>

        <div class="text-center">
            <a href="/register" class="text-decoration-none">¿No tienes cuenta? Regístrate</a>
        </div>

    </div>

</div>

<!-- Bootstrap JS -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

</body>
</html>
```
## HOME.HTML
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Registro</title>

    <!-- Bootstrap 5 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body class="bg-light">

<div class="container d-flex justify-content-center align-items-center vh-100">

    <div class="card shadow-lg p-4" style="min-width: 350px; max-width: 450px; width: 100%; border-radius: 12px;">

        <div class="text-center mb-4">
            <h3 class="fw-bold">Registro</h3>
            <p class="text-muted">Crea tu cuenta para comenzar</p>
        </div>

        <form method="POST">

            <div class="mb-3">
                <label class="form-label">Usuario</label>
                <input type="text" name="username" class="form-control" placeholder="Ingresa tu usuario" required>
            </div>

            <div class="mb-3">
                <label class="form-label">Correo</label>
                <input type="email" name="email" class="form-control" placeholder="Ingresa tu correo">
            </div>

            <div class="mb-3">
                <label class="form-label">Contraseña</label>
                <input type="password" name="password" class="form-control" placeholder="Ingresa tu contraseña" required>
            </div>

            <div class="d-grid mb-3">
                <button type="submit" class="btn btn-success btn-lg">
                    Registrar
                </button>
            </div>

        </form>

        <div class="text-center">
            <a href="/login" class="text-decoration-none">
                ¿Ya tienes cuenta? Ir al login
            </a>
        </div>

    </div>

</div>

<!-- Bootstrap JS -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

</body>
</html>
```

## REGISTER.HTML
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Registro</title>

    <!-- Bootstrap 5 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body class="bg-light">

<div class="container d-flex justify-content-center align-items-center vh-100">

    <div class="card shadow-lg p-4" style="min-width: 350px; max-width: 450px; width: 100%; border-radius: 12px;">

        <div class="text-center mb-4">
            <h3 class="fw-bold">Registro</h3>
            <p class="text-muted">Crea tu cuenta para comenzar</p>
        </div>

        <form method="POST">

            <div class="mb-3">
                <label class="form-label">Usuario</label>
                <input type="text" name="username" class="form-control" placeholder="Ingresa tu usuario" required>
            </div>

            <div class="mb-3">
                <label class="form-label">Correo</label>
                <input type="email" name="email" class="form-control" placeholder="Ingresa tu correo">
            </div>

            <div class="mb-3">
                <label class="form-label">Contraseña</label>
                <input type="password" name="password" class="form-control" placeholder="Ingresa tu contraseña" required>
            </div>

            <div class="d-grid mb-3">
                <button type="submit" class="btn btn-success btn-lg">
                    Registrar
                </button>
            </div>

        </form>

        <div class="text-center">
            <a href="/login" class="text-decoration-none">
                ¿Ya tienes cuenta? Ir al login
            </a>
        </div>

    </div>

</div>

<!-- Bootstrap JS -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

</body>
</html>
```

## EJECUTAR
```bash
python app.py
```

## ACCESO
http://127.0.0.1:5000

## MEJORAS FUTURAS
CSRF Protection, Flask-WTF, JWT, HTTPS, Rate limiting, 2FA, CAPTCHA, Roles, Auditoría, OWASP Top 10, SQLAlchemy, Docker, Nginx, Deploy Linux VPS
