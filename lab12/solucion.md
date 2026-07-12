# Laboratorio 12: Desarrollo Seguro de Aplicaciones - Logging y Errores

## ¿Por qué es un riesgo almacenar contraseñas en texto plano?
Si un atacante logra acceso a la base de datos mediante una inyección SQL (SQLi) o una fuga de respaldos, obtendrá de forma inmediata las credenciales de todos los usuarios. Peor aún, debido a la reutilización de contraseñas, el atacante podría vulnerar las cuentas de esos usuarios en otros servicios externos.

## ¿Qué es el Hashing y por qué usamos Werkzeug?
El *hashing* es un algoritmo criptográfico unidireccional que transforma un texto de longitud variable en una cadena de caracteres de longitud fija. Al ser unidireccional, es matemáticamente inviable revertir el *hash* para obtener la contraseña original. `Werkzeug` utiliza por defecto **Scrypt** o **PBKDF2** con un *salt* (sal) aleatorio, lo que mitiga los ataques de diccionario y las tablas de arcoíris (Rainbow Tables).

---

## 🛠️ Paso 1: Estructura del Proyecto

Crea la siguiente estructura de archivos en tu directorio de trabajo:

```text
laboratorio12/
│
├── app/
│   ├── templates/
│   │   ├── login.html
│   │   └── register.html
│   ├── app.py
│   └── requirements.txt
│
├── nginx/
│   └── default.conf       # Configuración de rutas del Proxy Inverso
│
├── logs/                  # Almacenamiento local persistente de logs de Flask
├── .env                   # Variables de entorno secretas
├── .gitignore             # Exclusión de credenciales para Git
├── Dockerfile             # Construcción de la imagen Flask
└── docker-compose.yml     # Orquestador central de la infraestructura

```

## 🔐 2. Variables de Entorno y Configuración Base
### 1. Creacion del archivo .env

```bash
cd laboratorio12
nano .env
```

Crea este archivo en la raíz para centralizar las credenciales. Configura contraseñas seguras aquí.

```text
# Entorno Flask
FLASK_ENV=production
SECRET_KEY=e9c7821685b8fae92e21b0f51d8b9e4a

# Credenciales Base de Datos
DB_ROOT_PASSWORD=Tu_contraseña
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=seguridad_db
```

### 3. 🐳 Configuración de Contenedores e Infraestructura

```bash
cd laboratorio12
nano Dockerfile
```
Copiamos esto dentro del archivo

```text
FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ .
EXPOSE 5000
CMD ["python", "app.py"]
```

Creamos la carpeta nginx y dentro de ella el archivo default.conf

```bash
cd laboratorio12
mkdir nginx
cd nginx
nano default.conf
```

nginx/default.conf

Nginx interceptará el tráfico. Mapeamos la raíz / hacia Flask y creamos una ruta reservada /phpmyadmin/ para administrar la base de datos de manera aislada.

```text
server {
    listen 80;
    server_name localhost;

    # Redirección al contenedor de la aplicación Flask
    location / {
        proxy_pass http://web:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Redirección al contenedor de phpMyAdmin
    location /phpmyadmin/ {
        proxy_pass http://myadmin:80/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```
Ahora creamos el archivo "docker-compose.yml" El motor definitivo. Implementa persistencia por volúmenes nombrados para la BD, carpetas compartidas para desarrollo y logs de Flask, políticas de reinicio automático y el healthcheck estricto de MariaDB para garantizar estabilidad.

```bash
cd laboratorio12
nano docker-compose.yml
```
Y dentro de ellos ponemos lo siguiente 

```text
version: '3.8'

services:
  # Servidor Web Externo (Proxy Inverso)
  nginx:
    image: nginx:alpine
    container_name: proxy_nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
    restart: unless-stopped
    depends_on:
      - web
      - myadmin
    networks:
      - net_produccion

  # Aplicación Flask (Backend)
  web:
    build: .
    container_name: app_flask
    environment:
      - FLASK_ENV=${FLASK_ENV}
      - SECRET_KEY=${SECRET_KEY}
      - DB_HOST=db_mariadb
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_NAME=${DB_NAME}
    restart: unless-stopped
    volumes:
      - ./app:/app             # Código vivo (volumen de desarrollo)
      - ./logs:/app/logs        # Persistencia de logs de seguridad
    depends_on:
      db_mariadb:
        condition: service_healthy
    networks:
      - net_produccion

  # Base de Datos Relacional MariaDB
  db_mariadb:
    image: mariadb:10.11
    container_name: db_mariadb
    restart: unless-stopped
    environment:
      MARIADB_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
      MARIADB_DATABASE: ${DB_NAME}
      MARIADB_USER: ${DB_USER}
      MARIADB_PASSWORD: ${DB_PASSWORD}
    volumes:
      - mariadb_data:/var/lib/mysql   # Persistencia absoluta de datos
    healthcheck:
      test: ["CMD", "healthcheck.sh", "--connect", "--innodb_initialized"]
      interval: 5s
      timeout: 5s
      retries: 5
      start_period: 10s
    networks:
      - net_produccion

  # Administrador Gráfico de Base de Datos (phpMyAdmin)
  myadmin:
    image: phpmyadmin:5.2
    container_name: admin_phpmyadmin
    restart: unless-stopped
    environment:
      - PMA_HOST=db_mariadb
      - PMA_ARBITRARY=0
      - PMA_ABSOLUTE_URI=/phpmyadmin/
    depends_on:
      db_mariadb:
        condition: service_healthy
    networks:
      - net_produccion

networks:
  net_produccion:
    driver: bridge

volumes:
  mariadb_data:
```

## 💻 Código de la Aplicación (Flask Seguro)
### 1. Creamos la carpeta app/ y dentro de ella el archivo requirements.txt

```bash
cd laboratorio12
mkdir app
cd app
nano requirements.txt
```
Dentro copiamos lo siguiente

```text
Flask==3.0.2
Werkzeug==3.0.1
pymysql==1.1.0
```

### 2. Creamos la carpeta app/ y dentro de ella el archivo app.py
Maneja conexiones limpias usando el healthcheck del orquestador. Captura excepciones de base de datos y escribe bitácoras en ./logs/app_secure.log.

```bash
cd laboratorio12/app
nano app.py
```
Dentro copiamos lo siguiente 

```python
import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler("logs/app_secure.log"), logging.StreamHandler()]
)

def get_db_connection():
    return pymysql.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_NAME'),
        cursorclass=pymysql.cursors.DictCursor
    )

def init_db():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL
                )
            """)
        conn.commit()
        logging.info("Persistencia e inicialización de tablas correcta.")
    except Exception as e:
        logging.error(f"Fallo en BD: {str(e)}")
    finally:
        conn.close()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        plaintext_password = request.form['password']
        
        logging.info(f"Registro solicitado para el usuario: '{username}'")
        hashed_password = generate_password_hash(plaintext_password, method='scrypt')
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            conn.commit()
            logging.info(f"Usuario '{username}' registrado exitosamente.")
            flash('Usuario creado correctamente.', 'success')
            return redirect(url_for('login'))
        except pymysql.err.IntegrityError:
            flash('El nombre de usuario ya existe.', 'danger')
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        
        logging.info(f"Intento de login para: '{username}'")
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                user = cursor.fetchone()
                
            if user and check_password_hash(user['password'], password_candidate):
                logging.info(f"Login Exitoso: '{username}'")
                flash(f'Bienvenido, {username}!', 'success')
            else:
                logging.warning(f"Login Fallido para: '{username}'")
                flash('Credenciales incorrectas.', 'danger')
        except Exception as e:
            logging.error(f"Error de sistema: {str(e)}")
            flash('Error interno controlado.', 'danger')
        finally:
            conn.close()
    return render_template('login.html')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
```
(Nota: Asegúrate de crear las interfaces HTML básicas dentro de app/templates/login.html y app/templates/register.html tal como se definieron previamente).

### 3. Login.html y registre.html

```bash
cd laboratorio12/app
mkdir templates
cd templates
nano login.html
```

Dentro copiamos lo siguiente 

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Acceso Seguro</title>
    <link rel="stylesheet" href="[https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css](https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css)">
</head>
<body class="bg-light container py-5" style="max-width: 420px;">
    <h3 class="text-center mb-4">Módulo de Autenticación</h3>
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }} text-center py-2">{{ message }}</div>
            {% endfor %}
         {% endif %}
    {% endwith %}
    <form method="POST" class="card p-4 shadow-sm">
        <div class="mb-3">
            <label class="form-label font-weight-bold">Identificador / Usuario:</label>
            <input type="text" name="username" class="form-control" autocomplete="off" required>
        </div>
        <div class="mb-3">
            <label class="form-label">Contraseña:</label>
            <input type="password" name="password" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-dark w-100">Iniciar Sesión</button>
        <div class="mt-3 text-center">
            <a href="/register" class="text-secondary small">Crear una cuenta nueva</a>
        </div>
    </form>
</body>
</html>

```

Despues creamos el register

```bash
cd laboratorio12/app/templates
nano register.html
```

y copiamos dentro

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Registro del Sistema</title>
    <link rel="stylesheet" href="[https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css](https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css)">
</head>
<body class="bg-light container py-5" style="max-width: 420px;">
    <h3 class="text-center mb-4">Registro Altamente Seguro</h3>
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }} text-center py-2">{{ message }}</div>
            {% endfor %}
         {% endif %}
    {% endwith %}
    <form method="POST" class="card p-4 shadow-sm">
        <div class="mb-3">
            <label class="form-label">Definir Usuario:</label>
            <input type="text" name="username" class="form-control" autocomplete="off" required>
        </div>
        <div class="mb-3">
            <label class="form-label">Definir Contraseña:</label>
            <input type="password" name="password" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-success w-100">Dar de Alta Usuario</button>
        <div class="mt-3 text-center">
            <a href="/login" class="text-secondary small">Regresar al portal de acceso</a>
        </div>
    </form>
</body>
</html>
```


## 🚀 5. Despliegue en Servidor VPS Paso a Paso (Debian 11)

###  Paso 1: Configurar el Cortafuegos de Red del VPS
En un entorno real con IP pública, cerramos todos los puertos excepto el puerto web estándar (80) y el puerto administrativo SSH (22). Nginx se encargará de distribuir las solicitudes internamente sin exponer los contenedores directamente a internet.

```bash
# 1. Instalar UFW
sudo apt update && sudo apt install ufw -y

# 2. Configurar políticas del firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 3. Abrir únicamente puertos seguros para el público
sudo ufw allow 22/tcp   # SSH administrativo
sudo ufw allow 80/tcp   # Tráfico Web hacia Nginx

# 4. Activar el Firewall
sudo ufw enable
```
### Paso 2: Descargar y Lanzar la Infraestructura
```bash
# 1. Clonar tu proyecto dentro del VPS
git clone <URL_TU_REPOSITORIO>
cd laboratorio12

# 2. Levantar toda la arquitectura multi-contenedor
sudo docker compose up --build -d

# 3. Comprobar que los cuatro contenedores estén activos y saludables
sudo docker compose ps
```
## 🌍 6. Cómo Acceder a los Servicios usando tu IP Pública

Una vez que el comando docker compose ps muestre todos los estados en Up (o healthy), abre cualquier navegador web en tu computadora e ingresa a través de los siguientes accesos:

### A. Para Ingresar a la Aplicación Web (Flask)
Nginx redirige las solicitudes de la raíz de forma automática. No necesitas especificar ningún puerto extra.

```bash
http://<TU_IP_PUBLICA_DEL_VPS>/
```
Ejemplo: http://198.51.100.42/

### B. Para Ingresar a phpMyAdmin (Gestor de Base de Datos)
Para auditar las tablas y verificar el almacenamiento de contraseñas con Hashing, accede a la subruta configurada en el Proxy Inverso:
```bash
http://<TU_IP_PUBLICA_DEL_VPS>/phpmyadmin/
```
Ejemplo: http://198.51.100.42/phpmyadmin/

### Credenciales de acceso a phpMyAdmin:
* Servidor (Server): db_mariadb (Este nombre es obligatorio porque Docker resuelve la red interna con este alias)
* Usuario (Username): root
* Contraseña (Password): La contraseña asignada en la variable ${DB_ROOT_PASSWORD} dentro de tu archivo .env.
