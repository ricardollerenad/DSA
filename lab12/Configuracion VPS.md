# 🐧 Guía de Configuración Inicial de Seguridad y Entorno en Debian 11

## 👤 Creación y Configuración de un Nuevo Usuario Seguro
El primer paso es actualizar los repositorios existentes, garantizar la presencia de la herramienta sudo y migrar la administración a una cuenta no privilegiada.

```bash
# 1. Actualizar el índice de paquetes y el sistema operativo
sudo apt update && sudo apt upgrade -y

# 2. Asegurar la instalación del paquete sudo (esencial en instalaciones limpias de Debian)
apt-get install sudo	

# 3. Asignar o cambiar la contraseña del usuario root actual
passwd

# 4. Crear el nuevo usuario del sistema (Reemplaza <<nombre_usuario>>)
sudo adduser <<nombre_usuario>> 

# 5. Agregar el usuario creado al grupo de administradores (sudo)
sudo usermod -a -G sudo <<nombre_usuario>>

# 6. Método alternativo/refuerzo para añadir al usuario al grupo sudo
sudo gpasswd -a <<nombre_usuario>> sudo
```

## ⚙️ Asignación de Privilegios Avanzados (Opcional/Raíz)
Si requieres que el usuario tenga reglas específicas de ejecución sin restricciones en el archivo de configuración de superusuarios, edita el archivo sudoers:

```bash
sudo nano /etc/sudoers
```

Agregar la siguiente línea debajo de las reglas de root:

```text
<<nombre_usuario>>    ALL=(ALL:ALL) ALL
```

## 🔒 Actividad 2: Bloqueo del Acceso Directo por Root (SSH)

Una vez que compruebes que tu nuevo usuario puede iniciar sesión y ejecutar comandos con sudo, es imperativo denegar el acceso remoto al usuario administrador global.

```bash
# 1. Editar el archivo de configuración del demonio SSH
sudo nano /etc/ssh/sshd_config
```

Dentro del archivo, busca la directiva PermitRootLogin y realiza el siguiente cambio:

```text
# Cambiar esto:
PermitRootLogin prohibit-password

# Por esto:
PermitRootLogin no
```

Reiniciar el servicio SSH para aplicar los cambios de seguridad

```bash
# 2. Reiniciar el servicio SSH para aplicar los cambios de seguridad
sudo /etc/init.d/ssh restart
```

# 📦 Instalación de Herramientas de Software Básicas

Instalación en bloque de utilidades de diagnóstico de red, monitorización de rendimiento, editores de texto y visualización de directorios indispensables para la administración.

```bash
sudo apt-get -y install \
  tree \
  wget \
  curl \
  nmap \
  net-tools \
  htop \
  btop \
  nano \
  vim
```

# ⏰ Configuración del Huso Horario (Timezone)

```bash
# 1. Establecer la zona horaria a la región de Perú (America/Lima)
sudo timedatectl set-timezone America/Lima

# 2. Comprobar que la configuración se aplicó correctamente
sudo timedatectl
```

# 🧱 Configuración del Cortafuegos (UFW)

```bash
# 1. Actualizar repositorios e instalar UFW
sudo apt update
sudo apt install ufw -y

# 2. Habilitar el inicio del servicio del Cortafuegos
sudo ufw enable

# 3. Permitir navegación Web Estándar y Segura
sudo ufw allow http 
sudo ufw allow https 

# 4. Permitir servicios del ecosistema y puertos específicos (SSH personalizado, Home Assistant, MQTT)
sudo ufw allow 22122
sudo ufw allow OpenSSH
sudo ufw allow 8123
sudo ufw allow 1883

# 5. Comprobar el estado actual de las reglas añadidas
sudo ufw status verbose

# 6. Recargar y reiniciar el servicio para consolidar los cambios en el Kernel
sudo ufw reload
sudo systemctl restart ufw
```

---
# Instalacion de Docker

## Paso 1: Actualizar el sistema e instalar dependencias previas
Primero, asegúrate de que tu lista de paquetes esté al día e instala algunas herramientas necesarias para que Debian pueda comunicarse con el repositorio de Docker de forma segura a través de HTTPS.

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg lsb-release
```

## Paso 2: Agregar la clave GPG oficial de Docker
La clave GPG sirve para verificar que los paquetes de Docker que vas a descargar sean auténticos y no hayan sido alterados.

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

## Paso 3: Configurar el repositorio oficial de Docker
Ahora le diremos a Debian exactamente de dónde debe descargar Docker. Este comando detectará automáticamente que estás en Debian 11 (bullseye) y configurará el canal estable:
```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

## Paso 4: Instalar el motor de Docker (Docker Engine) y Compose
Actualiza nuevamente tu índice de paquetes (para que reconozca el nuevo repositorio que acabamos de agregar) e instala Docker junto con el plugin de Docker Compose (que necesitas para el laboratorio).

```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## Paso 5: Verificar que Docker esté corriendo
Por defecto, el servicio de Docker debería iniciarse automáticamente. Puedes verificar su estado con:

```bash
sudo systemctl status docker
```
Para asegurarte de que todo el motor funciona bien, corre el clásico contenedor de prueba:

```bash
sudo docker run hello-world
```
