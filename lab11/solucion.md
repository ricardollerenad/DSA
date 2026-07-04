# ACTIVIDAD 1: PREPARACIÓN DEL ENTORNO PARA GESTIÓN SEGURA DE SESIONES

En este paso crearemos un entorno virtual para aislar las dependencias del proyecto  e instalaremos Flask junto con Flask-Login para el manejo de sesiones.

## 1. Crear la carpeta del proyecto y acceder a ella
'''bash
mkdir laboratorio11_seguridad
cd laboratorio11_seguridad
'''
## 2. Crear el entorno virtual (venv) para Python 3.10+
'''bash
python -m venv venv
venv\Scripts\activate
'''
## 3. Instalar Flask, Flask-Login y Werkzeug (para el hash seguro de contraseñas)
'''bash
pip install Flask flask-login Werkzeug
pip install flask-sqlalchemy pymysql
'''

## 4. Generar el archivo de dependencias congeladas (requirements.txt)
'''bash
pip freeze > requirements.txt
'''

# ACTIVIDAD 2: CONFIGURACIÓN DE MECANISMOS DE SESIÓN EN LA APLICACIÓN

Crearemos la estructura inicial de la aplicación Flask configurando 'LoginManager'. 
NOTA: Usaremos una 'SECRET_KEY' robusta. En producción, esta debe ser compleja e irreversible para evitar que los atacantes falsifiquen las cookies de sesión (Session Hijacking).

## 1. Crear el archivo principal de la aplicación
# app.py
'''python
import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# 1. Importar SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta_super_segura_12345'

# 2. Configurar la cadena de conexión a MySQL

Formato: mysql+pymysql://usuario:contraseña@servidor:puerto/nombre_base_datos
'''python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/laboratorio11_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
'''

# 3. Inicializar la base de datos
db = SQLAlchemy(app)

# Inicialización de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "warning"

## 4. NUEVO MODELO DE USUARIO (Mapeado a Tabla de MySQL)

# Ahora la clase hereda de db.Model (para MySQL) y UserMixin (para Flask-Login)
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False) # Almacena el hash seguro

@login_manager.user_loader
def load_user(user_id):
    # Antes: Buscaba en el diccionario en memoria
    # Ahora: Hace una consulta segura a la base de datos MySQL por ID
    return User.query.get(int(user_id))


## 5. CAMBIOS EN LAS RUTAS (Controladores)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Antes: users_db.get(username)
        # Ahora: Consulta segura a MySQL buscando por nombre de usuario
        user = User.query.filter_by(username=username).first()
        
        # La verificación del hash sigue siendo exactamente igual (Seguridad OWASP)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash("Credenciales inválidas. Intente nuevamente.", "danger")
            
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión de forma segura.", "success")
    return redirect(url_for('login'))

## 6. Crear las tablas automáticamente si no existen
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
'''
### Registrar un usuario de prueba en MySQL
Como ya no tienes el diccionario estático users_db, la primera vez que corras la aplicación la tabla users estará vacía. Puedes crear un script rápido o usar la terminal interactiva de Python para registrar al administrador con su contraseña hasheada:

'''python
from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Crear el usuario con la contraseña cifrada
    nuevo_usuario = User(username="admin", password_hash=generate_password_hash("password123"))
    db.session.add(nuevo_usuario)
    db.session.commit()
    print("Usuario administrador creado con éxito en MySQL.")
'''

# ACTIVIDAD 3: DISEÑO DE MODELO DE USUARIO PARA CONTROL DE SESIONES

Flask-Login requiere una clase de usuario con propiedades específicas. Utilizaremos 'UserMixin' que ya provee las implementaciones por defecto de:
is_authenticated, is_active, is_anonymous, y get_id().

# Añadir el siguiente bloque de código en app.py:
'''python
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username

# El 'user_loader' es fundamental: le dice a Flask-Login cómo recuperar un objeto de usuario
# a partir del ID almacenado en la cookie de sesión del navegador.
@login_manager.user_loader
def load_user(user_id):
    for username, data in users_db.items():
        if data['id'] == user_id:
            return User(user_id=data['id'], username=data['username'])
    return None
'''

# ACTIVIDAD 4: IMPLEMENTACIÓN DE AUTENTICACIÓN Y CREACIÓN DE SESIÓN

Diseñaremos el backend de inicio de sesión. Aplicaremos mitigación de riesgos: Usaremos 'check_password_hash' para mitigar ataques de temporización y fuerza bruta. Usaremos un mensaje genérico para evitar la enumeración de nombres de usuario.

## 1. Crear las carpetas para las vistas HTML
'''bash
mkdir templates
'''

## 2. Crear el formulario de Login (templates/login.html)
'''html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Iniciar Sesión Seguro</title>
</head>
<body>
    <h2>Control de Acceso</h2>
    
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, message in messages %}
          <p style="color: red;">[{{ category.upper() }}] {{ message }}</p>
        {% endfor %}
      {% endif %}
    {% endwith %}

    <form method="POST" action="{{ url_for('login') }}">
        <label>Usuario:</label>
        <input type="text" name="username" required autocomplete="off"><br><br>
        
        <label>Contraseña:</label>
        <input type="password" name="password" required><br><br>
        
        <button type="submit">Ingresar Sistema</button>
    </form>
</body>
</html>
'''

# 3. Agregar la lógica de la ruta Login a app.py
'''python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user_data = users_db.get(username)
        
        # PRINCIPIO DE SEGURIDAD: Validación unificada para evitar enumeración de usuarios
        # check_password_hash verifica de manera segura el hash almacenado contra el texto plano
        if user_data and check_password_hash(user_data['password_hash'], password):
            user_obj = User(user_id=user_data['id'], username=user_data['username'])
            login_user(user_obj) # Crea la sesión segura del usuario
            return redirect(url_for('dashboard'))
        else:
            # MITIGACIÓN: Mensaje genérico que no revela si falló el usuario o la contraseña
            flash("Credenciales inválidas. Intente nuevamente.", "error")
            
    return render_template('login.html')
'''

# ACTIVIDAD 5: PROTECCIÓN DE RUTAS MEDIANTE CONTROL DE SESIONES
Implementaremos una sección privada que requiere obligatoriamente una sesión activa. El decorador '@login_required' intercepta la petición y valida el estado de la sesión.

## 1. Crear la vista del panel privado (templates/dashboard.html)
'''python
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Panel Seguro (Dashboard)</title>
</head>
<body>
    <h1>Bienvenido al Sistema Seguro, {{ current_user.username }}!</h1>
    <p>Esta información está protegida contra accesos no autorizados por controles criptográficos de sesión.</p>
    <br>
    <a href="{{ url_for('logout') }}">Cerrar Sesión de Forma Segura</a>
</body>
</html>
'''

## 2. Implementar la ruta protegida en app.py
'''python
@app.route('/dashboard')
@login_required # Restringe el acceso. Si no está autenticado, redirige a '/login'
def dashboard():
    return render_template('dashboard.html')
'''
# ACTIVIDAD 6: IMPLEMENTACIÓN DE CIERRE SEGURO DE SESIÓN
Destrucción segura del identificador de sesión. Limpia las cookies del lado del cliente y revoca la validez de la sesión activa en el contexto del servidor.

# Añadir la ruta de cierre de sesión en app.py:
'''python
@app.route('/logout')
@login_required
def logout():
    logout_user() # Destruye y limpia la sesión activa de Flask-Login
    flash("Has cerrado sesión de forma segura.", "success")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
'''

# ACTIVIDAD 7: VALIDACIÓN DE LA GESTIÓN SEGURA DE SESIONES (QA PRUEBAS)
Para validar la robustez técnica del sistema implementado, realiza los siguientes pasos prácticos:

## Paso A: Ejecutar la aplicación
python app.py

## Paso B: Acceso sin autenticación
Abre una ventana de incógnito en tu navegador y escribe directamente: http://127.0.0.1:5000/dashboard
*REQUISITO EXIGIDO:* El servidor debe bloquear el acceso e interceptarte redirigiéndote a /login.

## Paso C: Inicio de sesión correcto
En el formulario ingresa: Usuario: admin | Contraseña: password123
*REQUISITO EXIGIDO:* La sesión se creará y serás redirigido al panel (/dashboard).

## Paso D: Cierre de sesión
Haz clic en "Cerrar Sesión de Forma Segura".
*REQUISITO EXIGIDO:* Volverás a /login y al intentar retroceder con el navegador al /dashboard, este volverá a bloquearte.



# Anexos

## Arquitectura de carpetas
'''bash
laboratorio11_seguridad/
│
├── venv/                       # Entorno virtual de Python (omitido en Git)
│
├── templates/                  # Vistas HTML (Bootstrap 5)
│   ├── login.html              # Formulario de acceso seguro
│   └── dashboard.html          # Panel privado protegido
│
├── .gitignore                  # Filtro para evitar subir basura o credenciales a Git
├── app.py                      # Archivo principal (Flask, Flask-Login y SQLAlchemy)
└── requirements.txt            # Dependencias del proyecto (Flask, PyMySQL, etc.)
'''
## app.py final
'''python
import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# ==========================================
# CONFIGURACIÓN DE SEGURIDAD
# ==========================================
# En producción, usa una clave compleja guardada en variables de entorno: os.environ.get('SECRET_KEY')
app.config['SECRET_KEY'] = 'mi_clave_secreta_super_segura_12345'

# Inicialización del Gestor de Sesiones
login_manager = LoginManager()
login_manager.init_app(app)

# Configuración de comportamiento para rutas protegidas
login_manager.login_view = 'login' # Redirige aquí si no está autenticado
login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."
login_manager.login_message_category = "info"


# ==========================================
# BASE DE DATOS SIMULADA (Usuarios Seguros)
# ==========================================
# Las contraseñas NUNCA se guardan en texto plano.
# generate_password_hash crea un hash criptográfico robusto.
users_db = {
    "admin": {
        "id": "1",
        "username": "admin",
        "password_hash": generate_password_hash("password123")
    },
    "user1": {
        "id": "2",
        "username": "user1",
        "password_hash": generate_password_hash("securepass2026")
    }
}


# ==========================================
# MODELO DE USUARIO (Flask-Login)
# ==========================================
# UserMixin hereda automáticamente: is_authenticated, is_active, is_anonymous, get_id()
class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    """Recupera el objeto Usuario desde la cookie de sesión del navegador"""
    for username, data in users_db.items():
        if data['id'] == user_id:
            return User(user_id=data['id'], username=data['username'])
    return None


# ==========================================
# CONTROLADORES Y RUTAS (Endpoints)
# ==========================================

@app.route('/')
def index():
    """Ruta de inicio pública"""
    return '<h1>Bienvenido a la página pública</h1><p><a href="/login">Ir al Login</a></p>'


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Manejo de inicio de sesión seguro"""
    # Si ya está logueado, lo mandamos directo al dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user_data = users_db.get(username)
        
        # SEGURIDAD: check_password_hash evita ataques de tiempo (Timing Attacks)
        if user_data and check_password_hash(user_data['password_hash'], password):
            user_obj = User(user_id=user_data['id'], username=user_data['username'])
            login_user(user_obj) # Crea la sesión en el servidor y la cookie en el cliente
            return redirect(url_for('dashboard'))
        else:
            # MITIGACIÓN OWASP: Mensaje genérico para evitar enumeración de nombres de usuario
            flash("Credenciales inválidas. Intente nuevamente.", "error")
            
    return render_template('login.html')


@app.route('/dashboard')
@login_required # PROTECCIÓN: Bloquea el acceso si no hay sesión activa
def dashboard():
    """Ruta Privada Protegida"""
    return render_template('dashboard.html')


@app.route('/logout')
@login_required
def logout():
    """Cierre de sesión seguro"""
    logout_user() # Destruye los datos de la sesión del usuario
    flash("Has cerrado sesión de forma segura.", "success")
    return redirect(url_for('login'))


# ==========================================
# EJECUCIÓN DEL SERVIDOR
# ==========================================
if __name__ == '__main__':
    # debug=True se usa solo en desarrollo para ver errores en tiempo real
    app.run(debug=True)
'''
## Tablas en la Base de datos 
'''sql 
-- 1. Crear la base de datos si no existe (con codificación UTF-8 para soporte de tildes y caracteres especiales)
CREATE DATABASE IF NOT EXISTS laboratorio11_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 2. Seleccionar la base de datos para trabajar en ella
USE laboratorio11_db;

-- 3. (OPCIONAL) Crear la tabla manualmente
-- Nota: 'db.create_all()' en Flask hace esto por ti, pero si prefieres asegurar la estructura exacta, corre este comando:
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
) ENGINE=InnoDB;

-- 4. Insertar el usuario administrador con un Hash de prueba seguro
-- IMPORTANTE: Este hash corresponde a la contraseña "password123" usando el algoritmo pbkdf2:sha256 de Werkzeug.
INSERT INTO users (username, password_hash) 
VALUES ('admin', 'pbkdf2:sha256:600000$uG7xR8Wz8mJ9$4e3f42c674bb96da60431bdf7f3efc29184ba5dfcd7f3e8b0a9442a6c0b9a9d7')
ON DUPLICATE KEY UPDATE username=username;
'''

⚠️ Notas de configuración importantes:
Credenciales en app.py: Asegúrate de que la línea de configuración en tu archivo de Python coincida con el usuario y contraseña de tu servidor local de MySQL:

## Cambia 'root' y 'password' por tus credenciales reales de MySQL
'''python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://usuario_mysql:contraseña_mysql@localhost:3306/laboratorio11_db'
'''

El Hash de la contraseña: El string largo que pusimos en el INSERT no es texto plano. Es el resultado cifrado. Cuando escribas admin y password123 en tu bonito formulario de Bootstrap, la función check_password_hash del backend validará que coincidan perfectamente.
