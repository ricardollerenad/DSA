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
from flask import Flask, render_template, request, redirect, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")

mysql = MySQL(app)

@app.route("/")
def home():
    return redirect("/login")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]

        if len(username) < 3:
            flash("Usuario inválido")
            return redirect("/register")

        password_hash = generate_password_hash(password)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios(username,email,password_hash) VALUES(%s,%s,%s)", (username,email,password_hash))
        mysql.connection.commit()
        cur.close()

        flash("Usuario registrado")
        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE username=%s", (username,))
        user = cur.fetchone()
        cur.close()

        if user:
            if check_password_hash(user[3], password):
                session["user"] = username
                flash("Bienvenido")
                return redirect("/dashboard")

        flash("Credenciales incorrectas")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return f"Bienvenido {session['user']}"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
```

## LOGIN.HTML
```html
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
<h2>Login Seguro</h2>
<form method="POST">
<input type="text" name="username" placeholder="Usuario" required><br><br>
<input type="password" name="password" placeholder="Password" required><br><br>
<button type="submit">Ingresar</button>
</form>
<a href="/register">Registrarse</a>
</body>
</html>
```

## REGISTER.HTML
```html
<!DOCTYPE html>
<html>
<head><title>Registro</title></head>
<body>
<h2>Registro</h2>
<form method="POST">
<input type="text" name="username" placeholder="Usuario" required><br><br>
<input type="email" name="email" placeholder="Correo"><br><br>
<input type="password" name="password" placeholder="Password" required><br><br>
<button type="submit">Registrar</button>
</form>
<a href="/login">Ir al login</a>
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
