# Guía de Resolución: Laboratorio N° 7 - Riesgo y Control con Bandit

**Curso:** Desarrollo de Aplicaciones Seguras (Python y Flask)
**Herramienta:** Bandit (SAST - Static Application Security Testing)

---

## 📋 Requisitos Previos y Control de Versiones (Git)

Antes de iniciar las actividades, recuerda las reglas de seguridad de la guía: mantener el repositorio **privado** y registrar cada avance con Git antes y después de corregir vulnerabilidades.

```bash
# 1. Inicializar repositorio Git (si aún no lo tienes en tu carpeta de proyecto)
git init

# 2. Verificar el estado actual de tus archivos
git status

# 3. Guardar el estado inicial (con el código antes de auditar)
git add .
git commit -m "chore: estado inicial del proyecto antes del análisis SAST"
```

---

## 🛠️ ACTIVIDAD 1: Preparación del Entorno para Evaluación de Riesgos con Bandit

### Paso N° 1: Habilitar el entorno virtual e instalar Bandit

Asegúrate de estar en la raíz de tu proyecto en la terminal.

```bash
# Crear entorno virtual (en caso no exista)
python -m venv venv

# Activar entorno virtual en Windows (PowerShell / CMD):
.\venv\Scripts\activate

# Activar entorno virtual en Linux / macOS:
source venv/bin/activate

# Instalar Flask (si no está instalado) y Bandit
pip install flask bandit
```

### Paso N° 2: Verificar su instalación

Ejecuta el siguiente comando para confirmar que Bandit funciona correctamente:

```bash
bandit --version
```

> 📸 **EVIDENCIA REQUERIDA:** Toma una captura de pantalla de tu terminal mostrando el resultado del comando `bandit --version` (ej. `bandit 1.7.x`).

### 💻 Código de Ejemplo (Opcional - Si no tienes un proyecto Flask aún)

Si ya tienes tu propio código en Flask, omite este bloque y pasa directamente a la Actividad 2. Si necesitas un archivo para practicar, crea un archivo llamado `app.py` con el siguiente código intencionalmente vulnerable:

```python
# app.py (CÓDIGO INICIAL CON VULNERABILIDADES)
import os
import subprocess
from flask import Flask, request

app = Flask(__name__)

# VULNERABILIDAD 1 (B105): Contraseña / Secret Key hardcodeada en el código fuente
app.secret_key = "super_secreto_hardcodeado_12345"

@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    # VULNERABILIDAD 2 (B602 / B605): Uso inseguro de shell=True (Riesgo de Command Injection)
    resultado = subprocess.check_output(f"ping -c 1 {host}", shell=True)
    return resultado

if __name__ == "__main__":
    # VULNERABILIDAD 3 (B201 / B104): Modo debug activo en producción y enlace a todas las interfaces
    app.run(host="0.0.0.0", port=5000, debug=True)
```

---

## 🔍 ACTIVIDAD 2: Ejecución de Análisis para Identificación de Riesgos de Seguridad

### Paso N° 1: Ejecutar el análisis en la carpeta del proyecto

> **Nota:** En la guía del laboratorio figura `bandit -r`, pero es obligatorio indicarle el punto `.` al final para que escanee el directorio actual y excluya la carpeta del entorno virtual `venv` con `-x`.

```bash
# Analizar recursivamente el proyecto actual excluyendo la carpeta del entorno virtual
bandit -r . -x ./venv
```

### Paso N° 2: Analizar el reporte generado

En la consola observarás bloques llamados `>> Issue:` que indican:

- Código y descripción del problema (ej. `[B201:flask_debug_true]`).
- **Severity** (Low, Medium, High) y **Confidence**.
- **Location** (archivo y número de línea exacto).

> 📸 **EVIDENCIA REQUERIDA:** Toma una captura de pantalla de la terminal donde se observen al menos **3 vulnerabilidades o advertencias** detectadas por Bandit.

---

## 📊 ACTIVIDAD 3: Evaluación e Interpretación de Riesgos Detectados

Con base en los resultados obtenidos en la Actividad 2, completa la tabla de tu documento. Aquí tienes un ejemplo basado en el código de prueba anterior; ajústalo a las líneas reales de tu proyecto:

| Vulnerabilidad detectada | Archivo | Línea | Severidad | Descripción |
|---|---|---|---|---|
| `B201: flask_debug_true` | `app.py` | 19 | High | La aplicación Flask se ejecuta con `debug=True`, lo que expone el depurador interactivo Werkzeug y permite ejecución remota de código. |
| `B602: subprocess_popen_with_shell_equals_true` | `app.py` | 14 | High | Ejecución de subprocesos con `shell=True` concatenando entradas del usuario, permitiendo inyección de comandos del sistema operativo. |
| `B105: hardcoded_password_string` | `app.py` | 8 | Low | Uso de una clave secreta (`secret_key`) escrita directamente en el código fuente, facilitando su exposición en el repositorio. |

---

## 🛡️ ACTIVIDAD 4: Aplicación de Controles Básicos para Mitigar Vulnerabilidades

### Paso N° 1: Modificar el código afectado

Corrige **al menos dos** vulnerabilidades aplicando controles de seguridad adecuados (variables de entorno, desactivación de debug, eliminación de `shell=True`, etc.).

```python
# app.py (CÓDIGO CORREGIDO Y SEGURO)
import os
import subprocess
from flask import Flask, request

app = Flask(__name__)

# MITIGACIÓN 1: Obtener la clave secreta desde una variable de entorno (o generar una aleatoria segura)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(24))

@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    # MITIGACIÓN 2: Pasar argumentos como lista y desactivar shell=True para evitar Command Injection
    resultado = subprocess.check_output(["ping", "-c", "1", host], shell=False)
    return resultado

if __name__ == "__main__":
    # MITIGACIÓN 3: Desactivar el modo debug y restringir el host a localhost (127.0.0.1)
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    app.run(host="127.0.0.1", port=5000, debug=debug_mode)
```

### Paso N° 2: Ejecutar nuevamente Bandit y registrar en Git

Vuelve a ejecutar el análisis para comprobar que las alertas críticas desaparecieron:

```bash
# 1. Re-ejecutar Bandit para verificar las correcciones
bandit -r . -x ./venv

# 2. Guardar los cambios mitigados en Git (cumpliendo la norma de trazabilidad)
git add app.py
git commit -m "fix(security): mitigar vulnerabilidades detectadas por Bandit (debug, shell=True y secret_key)"
```

> 📸 **EVIDENCIA REQUERIDA:** Adjunta dos capturas:
> 1. Captura del reporte generado por Bandit **antes** de la corrección.
> 2. Captura del reporte generado por Bandit **después** de la corrección.

---

## 📄 ACTIVIDAD 5: Elaboración de Reporte de Riesgos y Controles de Seguridad

### Paso N° 1: Generar reporte en archivo

Exporta los resultados de Bandit a un archivo de texto plano llamado `reporte_bandit.txt`:

```bash
# Generar el reporte en formato TXT excluyendo el entorno virtual
bandit -r . -x ./venv -f txt -o reporte_bandit.txt
```

### Paso N° 2: Revisar el archivo generado

Puedes abrir el archivo en VS Code o visualizarlo directamente desde la terminal:

```bash
# Ver el contenido del archivo en Windows (PowerShell):
Get-Content reporte_bandit.txt

# Ver el contenido del archivo en Linux / macOS:
cat reporte_bandit.txt
```

> 📸 **EVIDENCIA REQUERIDA:** Adjunta una captura del archivo `reporte_bandit.txt` abierto y añade una breve explicación.

**Explicación sugerida:**

> "El archivo `reporte_bandit.txt` documenta de forma estructurada la auditoría estática realizada por Bandit. Contiene la fecha y hora del escaneo, los archivos analizados, el detalle de cada hallazgo (incluyendo su identificador CWE, severidad, nivel de confianza y fragmento de código afectado) y un resumen métrico final con el total de líneas de código evaluadas y la cantidad de vulnerabilidades agrupadas por nivel de riesgo."
