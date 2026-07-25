# Despliegue de Aplicación Flask en VPS con Dominio, NGINX, Docker y HTTPS

## Configuración completa de dominio apuntando a servidor VPS

---

# 1. Introducción

Este documento describe el procedimiento completo para desplegar una aplicación Flask contenerizada en un servidor VPS utilizando:

- Debian 12.
- Docker.
- Docker Compose.
- NGINX como Reverse Proxy.
- Dominio propio.
- Certificado SSL mediante Let's Encrypt.
- HTTPS.

La arquitectura final será:

```
Usuario

   |

   v

Dominio

https://midominio.com

   |

   v

NGINX

   |

   v

Docker Flask

   |

   v

MariaDB

```

---

# 2. Requisitos Previos

## 2.1 Dominio registrado

Se requiere contar con un dominio:

Ejemplo:

```
midominio.com
```

Proveedores:

- Cloudflare Registrar.
- Namecheap.
- GoDaddy.
- Hostinger.
- NIC Perú.

---

## 2.2 Servidor VPS

Servidor recomendado:

```
Sistema Operativo:

Debian 12


IP Pública:

200.100.50.25

```

Acceso:

```bash
ssh root@200.100.50.25
```

---

# 3. Configuración DNS del Dominio

El dominio debe apuntar hacia la IP pública del servidor.

---

# 3.1 Obtener IP pública del VPS

Ejecutar:

```bash
curl ifconfig.me
```

Ejemplo:

```
200.100.50.25
```

---

# 3.2 Crear Registro A

Ingresar al panel DNS del proveedor del dominio.

Crear:

| Tipo | Nombre | Valor |
|---|---|---|
| A | @ | IP VPS |

Ejemplo:

```
Tipo:

A


Nombre:

@


Valor:

200.100.50.25

```

Resultado:

```
midominio.com

        |

        v

200.100.50.25

```

---

# 3.3 Crear Registro www

Agregar:

| Tipo | Nombre | Valor |
|-|-|-|
| A | www | IP VPS |

Ejemplo:

```
www.midominio.com

        |

        v

200.100.50.25

```

---

# 3.4 Validar DNS

Desde tu computadora:

## Windows

```powershell
nslookup midominio.com
```

## Linux

```bash
dig midominio.com
```

Resultado esperado:

```
Address:

200.100.50.25
```

---

# 4. Preparación del Servidor Debian 12

Actualizar paquetes:

```bash
apt update

apt upgrade -y
```

---

Instalar herramientas:

```bash
apt install \
curl \
git \
nano \
ufw \
-y
```

---

# 5. Configuración Firewall

Permitir SSH:

```bash
ufw allow ssh
```

Permitir HTTP:

```bash
ufw allow 80/tcp
```

Permitir HTTPS:

```bash
ufw allow 443/tcp
```

Activar firewall:

```bash
ufw enable
```

Verificar:

```bash
ufw status
```

Resultado:

```
22/tcp  ALLOW

80/tcp  ALLOW

443/tcp ALLOW
```

---

# 6. Instalación de Docker

Instalar dependencias:

```bash
apt install \
ca-certificates \
curl \
gnupg \
-y
```

Crear directorio:

```bash
install -m 0755 -d /etc/apt/keyrings
```

Agregar llave Docker:

```bash
curl -fsSL https://download.docker.com/linux/debian/gpg \
-o /etc/apt/keyrings/docker.asc
```

Actualizar:

```bash
apt update
```

Instalar Docker:

```bash
apt install \
docker-ce \
docker-compose-plugin \
-y
```

---

# 7. Verificar Docker

Versión:

```bash
docker --version
```

Ejemplo:

```
Docker version 28.x
```

---

Docker Compose:

```bash
docker compose version
```

Resultado:

```
Docker Compose version v2.x
```

---

# 8. Crear estructura del proyecto

Ubicación recomendada:

```
/var/www
```

Crear:

```bash
mkdir /var/www
```

Ingresar:

```bash
cd /var/www
```

---

Clonar proyecto:

```bash
git clone https://github.com/usuario/proyecto-csrf.git
```

Ingresar:

```bash
cd proyecto-csrf
```

---

# 9. Configuración de variables de entorno

Crear archivo:

```bash
nano .env
```

Contenido:

```env
SECRET_KEY=clave_segura_produccion_123456


DB_HOST=mariadb

DB_NAME=laboratorio_csrf

DB_USER=admin

DB_PASSWORD=Admin123456


FLASK_ENV=production
```

---

# 10. Configuración NGINX Reverse Proxy

Arquitectura:

```
Internet

   |

   v

NGINX :80 / :443

   |

   v

Flask :5000

```

---

Crear archivo:

```
nginx/nginx.conf
```

Contenido:

```nginx
server {


listen 80;


server_name midominio.com www.midominio.com;



location / {


proxy_pass http://flask:5000;



proxy_set_header Host $host;


proxy_set_header X-Real-IP $remote_addr;


proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;


proxy_set_header X-Forwarded-Proto $scheme;


}


}
```

Cambiar:

```
midominio.com
```

por tu dominio real.

---

# 11. Levantar aplicación

Construir:

```bash
docker compose build
```

Ejecutar:

```bash
docker compose up -d
```

---

# 12. Verificar servicios

Mostrar contenedores:

```bash
docker ps
```

Debe aparecer:

```
nginx

flask

mariadb

phpmyadmin

```

---

# 13. Prueba inicial

Abrir:

```
http://midominio.com
```

Debe cargar:

```
Sistema de Quejas Seguro
```

---

# Continuará en PARTE 2

Incluye:

- Configuración HTTPS.
- Certbot.
- Let's Encrypt.
- Renovación automática.
- Docker Compose final producción.
- Arquitectura final.
- Checklist de despliegue.

# PARTE 2 - CONFIGURACIÓN HTTPS, CERTIFICADO SSL Y DESPLIEGUE FINAL

Continuación del documento:

`despliegue-dominio-vps.md`

---

# 14. Configuración HTTPS con Certbot y Let's Encrypt

## Objetivo

Configurar un certificado SSL gratuito para habilitar:
```
https://midominio.com
```

permitiendo:

- Comunicación cifrada.
- Protección de credenciales.
- Mayor seguridad del laboratorio.
- Cumplimiento de buenas prácticas DevSecOps.

---

# 15. Instalación de Certbot

Instalar Certbot y el módulo para NGINX:

```bash
apt update
apt install certbot python3-certbot-nginx -y
# Verificar instalación:
certbot --version
# Resultado esperado:
certbot 2.x.x
```
#  16. Solicitar Certificado SSL
Ejecutar:
```bash
certbot --nginx \
-d midominio.com \
-d www.midominio.com
```

# 17. Probar HTTPS
Abrir navegador:
