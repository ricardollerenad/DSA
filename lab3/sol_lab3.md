# 🔐 Laboratorio SSDLC - SQL Injection con Python + Flask + MySQL (XAMPP)

# 🎯 Objetivo

En este laboratorio aprenderás a:

- 🗄️ Crear una base de datos con MySQL
- 💻 Desarrollar una aplicación vulnerable
- ⚠️ Ejecutar un ataque SQL Injection
- 🛡️ Mitigar la vulnerabilidad usando consultas parametrizadas

---

# 🛠️ Tecnologías utilizadas

- 🐍 Python
- 🌐 Flask
- 🗄️ MySQL
- 📦 XAMPP
- 💻 VS Code
- 🪟 Windows

---

# ⚙️ PASO 1: SETUP - Preparación del entorno

## 🧪 0.1 Verificar instalación de Python

```bash
python --version
pip --version


## 🧪 0.2 Activar entorno virtual 
```bash
python -m venv venv
Set-ExecutionPolicy Unrestricted -Scope Process
venv\Scripts\activate
python -m pip install --upgrade pip

## 🧪 0.3 Instalar librerias
```bash
pip install flask
pip install mysql-connector-python
pip freeze > requirements.txt

---

# 🗄️ ACTIVIDAD 1 - CREACIÓN DE BASE DE DATOS

# 📄 PASO 1: Crear archivo database.py

Crear archivo:

```txt
database.py
```

Agregar:

```python
import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

cursor = conexion.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS usuarios_db")

conexion.database = "usuarios_db"

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
id INT AUTO_INCREMENT PRIMARY KEY,
usuario VARCHAR(50),
password VARCHAR(50)
)
""")

cursor.execute("INSERT INTO usuarios(usuario,password) VALUES('admin','1234')")
cursor.execute("INSERT INTO usuarios(usuario,password) VALUES('usuario','abcd')")

conexion.commit()
conexion.close()

print("Base de datos creada")
```

---

# ▶️ PASO 2: Ejecutar script

Ejecutar:

```bash
python database.py
```

Resultado esperado:

```txt
Base de datos creada
```

---

# 🔍 PASO 3: Verificar base de datos

Abrir navegador:

```txt
http://localhost/phpmyadmin
```

Verificar:

```txt
usuarios_db
```

Tabla:

```txt
usuarios
```

---

# 💻 ACTIVIDAD 2 - LOGIN VULNERABLE

# 📄 PASO 1: Crear archivo app.py

Crear archivo:

```txt
app.py
```

Agregar:

```python
from flask import Flask, request

import mysql.connector

app = Flask(__name__)

@app.route('/')
def login():

    return '''
    <h2>Login SSDLC</h2>

    <form method="POST" action="/ingresar">

        Usuario:
        <input type="text" name="usuario"><br><br>

        Password:
        <input type="password" name="password"><br><br>

        <input type="submit" value="Ingresar">

    </form>
    '''

@app.route('/ingresar', methods=['POST'])
def ingresar():

    usuario = request.form['usuario']
    password = request.form['password']

    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="usuarios_db"
    )

    cursor = conexion.cursor()

    consulta = f"SELECT * FROM usuarios WHERE usuario='{usuario}' AND password='{password}'"

    cursor.execute(consulta)

    resultado = cursor.fetchone()

    conexion.close()

    if resultado:
        return "<h1>✅ Acceso concedido</h1>"
    else:
        return "<h1>❌ Acceso denegado</h1>"

app.run(debug=True)
```

---

# ▶️ PASO 2: Ejecutar aplicación

Ejecutar:

```bash
python app.py
```

Resultado esperado:

```txt
Running on http://127.0.0.1:5000
```

---

# 🌐 PASO 3: Abrir navegador

Abrir:

```txt
http://127.0.0.1:5000
```

---

# 🔑 PASO 4: Probar login normal

Usar:

```txt
Usuario: admin
Password: 1234
```

Resultado esperado:

```txt
✅ Acceso concedido
```

---

# ⚠️ ACTIVIDAD 3 - SQL INJECTION

# 💥 PASO 1: Ejecutar ataque

En usuario escribir:

```sql
' OR '1'='1
```

En password escribir:

```sql
' OR '1'='1
```

---

# 🧪 PASO 2: Resultado esperado

Resultado:

```txt
✅ Acceso concedido
```

---

# 🛡️ ACTIVIDAD 4 - MITIGACIÓN

# ✏️ PASO 1: Modificar consulta vulnerable

Reemplazar:

```python
consulta = f"SELECT * FROM usuarios WHERE usuario='{usuario}' AND password='{password}'"

cursor.execute(consulta)
```

Por:

```python
consulta = "SELECT * FROM usuarios WHERE usuario=%s AND password=%s"

cursor.execute(consulta, (usuario, password))
```

---

# 💾 PASO 2: Guardar cambios

Guardar:

```txt
CTRL + S
```

---

# ▶️ PASO 3: Ejecutar nuevamente

```bash
python app.py
```

---

# 💥 PASO 4: Repetir ataque SQL Injection

Usar nuevamente:

```sql
' OR '1'='1
```

---

# ✅ PASO 5: Resultado esperado

Resultado:

```txt
❌ Acceso denegado
```

---

# 📂 ESTRUCTURA FINAL DEL PROYECTO

```txt
Laboratorio_SSDLC/
│
├── app.py
├── database.py
```

---

# 💻 COMANDOS UTILIZADOS

## 📦 Instalar dependencias

```bash
pip install flask
pip install mysql-connector-python
```

## 🗄️ Ejecutar base de datos

```bash
python database.py
```

## 🌐 Ejecutar aplicación

```bash
python app.py
```

---

# 📸 EVIDENCIAS RECOMENDADAS

Tomar capturas de:

- 💻 VS Code con el código
- 🖥️ Terminal ejecutando scripts
- 🗄️ phpMyAdmin mostrando la BD
- 🌐 Login funcionando
- ⚠️ SQL Injection exitoso
- 🛡️ Mitigación funcionando
- ✅ SQL Injection bloqueado

---

# 🎉 FIN DEL LABORATORIO
