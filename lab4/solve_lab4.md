
# 🧪 Laboratorio Web Vulnerable + XSS + SQL Injection (Flask + MySQL)

## 👨‍🏫 Autor: Docente Programador
## 🎯 Objetivo: Aprender vulnerabilidades web (SQL Injection + XSS) y estructura segura de proyectos Flask

---

# ⚙️ SETUP DEL ENTORNO

## 1. Crear entorno virtual

```bash
python -m venv venv
venv\Scripts\activate
```

## 2. Actualizar pip

```bash
python -m pip install --upgrade pip
```

## 3. Instalar dependencias

```bash
pip install flask
pip install bcrypt
pip install mysql-connector-python
pip install python-dotenv
```

## 4. Guardar dependencias

```bash
pip freeze > requirements.txt
```

---

# 📁 ESTRUCTURA DEL PROYECTO

```
laboratorio_web_vulnerable/
│
├── app.py
├── db.py
├── requirements.txt
│
├── templates/
│   ├── login.html
│   └── sugerencias.html
│
└── static/
    └── style.css
```

---

# 🗄️ PREPARACIÓN DE BASE DE DATOS (MySQL)

## Crear base de datos

```sql
CREATE DATABASE laboratorio_xss;
USE laboratorio_xss;
```

## Tabla usuarios

```sql
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50),
    password VARCHAR(255)
);
```

## Tabla sugerencias

```sql
CREATE TABLE sugerencias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mensaje TEXT
);
```

---

# 🐍 db.py

```python
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="laboratorio"
    )
```

---

# 🧠 app.py (VERSIÓN VULNERABLE)

```python
from flask import Flask, render_template, request, redirect, session
from db import get_connection

app = Flask(__name__)
app.secret_key = "123"

# =========================
# LOGIN (SQL INJECTION)
# =========================
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        user = request.form["usuario"]
        pwd = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor()

        # ❌ VULNERABLE: concatenación directa
        query = f"SELECT * FROM usuarios WHERE usuario='{user}' AND password='{pwd}'"
        cursor.execute(query)

        result = cursor.fetchone()

        if result:
            session["user"] = user
            return redirect("/sugerencias")

    return render_template("login.html")


# =========================
# SUGERENCIAS (XSS)
# =========================
@app.route("/sugerencias", methods=["GET", "POST"])
def sugerencias():

    if "user" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        mensaje = request.form["mensaje"]

        # ❌ VULNERABLE A XSS
        cursor.execute(f"INSERT INTO sugerencias (mensaje) VALUES ('{mensaje}')")
        conn.commit()

    cursor.execute("SELECT mensaje FROM sugerencias")
    datos = cursor.fetchall()

    return render_template("sugerencias.html", datos=datos)


if __name__ == "__main__":
    app.run(debug=True)
```

---

# 🌐 login.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>

<h1>Login</h1>

<form method="POST">
    <input type="text" name="usuario" placeholder="Usuario">
    <input type="password" name="password" placeholder="Password">
    <button type="submit">Ingresar</button>
</form>

</body>
</html>
```

---

# 💬 sugerencias.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>Buzón de sugerencias</title>
</head>
<body>

<h1>Buzón de sugerencias</h1>

<form method="POST">
    <input type="text" name="mensaje" placeholder="Escribe tu sugerencia">
    <button type="submit">Enviar</button>
</form>

<hr>

<h2>Mensajes:</h2>

<!-- ❌ VULNERABLE A XSS -->
{% for m in datos %}
    <!-- <p>{{ m[0] }}</p> --> 
    <p>{{ m[0] | safe }}</p>
{% endfor %}

</body>
</html>
```

---

# 💣 SIMULACIÓN DE ATAQUES

## 🔴 SQL INJECTION

```text
usuario: ' OR '1'='1
password: ' OR '1'='1
```

---

## 🔴 XSS (Cross-Site Scripting)

```html
<script>alert("XSS ejecutado")</script>
```

```html
<script>alert(document.cookie)</script>
```

---

# 🎯 CONCLUSIÓN

Este laboratorio permite comprender:

- SQL Injection
- XSS
- Arquitectura Flask + MySQL
- Importancia de la validación de datos
- Riesgos de seguridad web

⚠️ SISTEMA INTENCIONALMENTE VULNERABLE PARA APRENDIZAJE

