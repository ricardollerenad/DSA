# DESPLIEGUE EN DOCKER

## PASO N.º 1: Instalar VirtualBox y configurar Debian 12

- Instalar VirtualBox. 
- Crear una máquina virtual con Debian 12. [Ver enlace](https://www.youtube.com/watch?v=BdWmwJzp8OI)
- Configurar la red en modo **Adaptador Puente (Bridge Adapter)**. [configurar modo brige](https://www.youtube.com/watch?v=V4X-grdifus)
- Habilitar el acceso a Internet.
- Actualizar el sistema:

```bash
sudo apt update && sudo apt upgrade -y
```

- Instalar OpenSSH Server:

```bash
sudo apt install -y openssh-server
```

- Instalar y habilitar UFW:

```bash
sudo apt install -y ufw
sudo ufw allow 22/tcp
sudo ufw enable
sudo ufw status
```

### ✅ CHECKPOINT

Verificar la dirección IP del servidor:

```bash
ip a
```

Comprobar que el servicio SSH esté activo:

```bash
sudo systemctl status ssh
```

---

# PASO N.º 2: Conectarse al servidor por SSH

Desde otra computadora ejecutar:

```bash
ssh nombre_usuario@IP_DEL_SERVIDOR
```

Ejemplo:

```bash
ssh administrador@192.168.1.100
```

Aceptar la huella digital del servidor cuando sea solicitada.

---

# PASO N.º 3: Instalar Docker

Ejecutar los siguientes comandos en el orden indicado.

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y ca-certificates curl gnupg lsb-release

sudo install -m 0755 -d /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/debian/gpg | \
sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/debian \
$(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update

sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### Agregar el usuario al grupo Docker

Para evitar utilizar `sudo` en cada comando:

```bash
sudo usermod -aG docker $USER
```

Cerrar la sesión SSH y volver a ingresar.

---

## ✅ CHECKPOINT: Verificar Docker

```bash
docker --version
docker compose version
sudo systemctl status docker
docker run hello-world
```

---

# PASO N.º 4: Copiar el proyecto al servidor

Puede hacerse mediante Git:

```bash
git clone URL_DEL_REPOSITORIO
cd nombre_del_proyecto
```

O copiando los archivos mediante SCP:

```bash
scp -r carpeta_proyecto usuario@IP_DEL_SERVIDOR:/home/usuario/
```

---

# PASO N.º 5: Verificar el archivo docker-compose.yml

Antes de levantar el proyecto comprobar que exista:

```bash
ls
```

Debe aparecer:

```text
docker-compose.yml
```

o

```text
compose.yml
```

---

# PASO N.º 6: Desplegar la aplicación

Construir y levantar los contenedores:

```bash
docker compose up -d
```

Si es el primer despliegue o hubo cambios en la imagen:

```bash
docker compose up -d --build
```

---

## ✅ CHECKPOINT: Verificar el despliegue

Ver los contenedores ejecutándose:

```bash
docker ps
```

Ver todos los contenedores:

```bash
docker ps -a
```

Ver los logs:

```bash
docker compose logs
```

Logs en tiempo real:

```bash
docker compose logs -f
```

---

# PASO N.º 7: Administrar los contenedores

Detener la aplicación:

```bash
docker compose down
```

Reiniciarla:

```bash
docker compose restart
```

Volver a levantarla:

```bash
docker compose up -d
```

---

# PASO N.º 8: Verificar acceso desde el navegador

Abrir en un navegador:

```text
http://IP_DEL_SERVIDOR
```

Si la aplicación utiliza otro puerto:

```text
http://IP_DEL_SERVIDOR:PUERTO
```

Ejemplo:

```text
http://192.168.1.100:8080
```

Si no responde, verificar:

- Que el contenedor esté en ejecución (`docker ps`).
- Que el puerto esté publicado en `docker-compose.yml`.
- Que UFW permita el puerto correspondiente.
- Que la red de la máquina virtual esté configurada como Adaptador Puente.
