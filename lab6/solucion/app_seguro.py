# ==========================================
# IMPORTACIONES PRINCIPALES DE FLASK
# ==========================================

from flask import Flask, render_template

# FlaskForm permite crear formularios seguros con CSRF integrado
from flask_wtf import FlaskForm

# Protección CSRF global
from flask_wtf.csrf import CSRFProtect

# Campos del formulario (SIN EmailField para evitar error email_validator)
from wtforms import StringField, SubmitField

# Validadores básicos
from wtforms.validators import DataRequired


# ==========================================
# INICIALIZACIÓN DE LA APP FLASK
# ==========================================

app = Flask(__name__)


# ==========================================
# SECRET_KEY (IMPORTANTE PARA CSRF)
# ==========================================
# Esta clave se usa para:
# - Firmar sesiones
# - Generar tokens CSRF
# - Validar seguridad de formularios
#
# Si cambia, los tokens CSRF anteriores dejan de funcionar
# ==========================================

app.config['SECRET_KEY'] = 'clave_super_secreta_lab_csrf_2026'


# ==========================================
# ACTIVAR PROTECCIÓN CSRF GLOBAL
# ==========================================
# Esto obliga a que TODA petición POST
# tenga un token CSRF válido
# ==========================================

csrf = CSRFProtect(app)


# ==========================================
# FORMULARIO SEGURO
# ==========================================

class RegistroForm(FlaskForm):

    # Campo nombre (obligatorio)
    nombre = StringField(
        'Nombre',
        validators=[DataRequired()]
    )

    # Campo correo (como texto simple para evitar errores)
    correo = StringField(
        'Correo',
        validators=[DataRequired()]
    )

    # Botón de envío
    enviar = SubmitField('Registrar')


# ==========================================
# RUTA PRINCIPAL
# ==========================================

@app.route('/', methods=['GET', 'POST'])
def inicio():

    # Crear instancia del formulario
    form = RegistroForm()

    # validate_on_submit():
    # - Verifica si es POST
    # - Verifica campos
    # - VERIFICA TOKEN CSRF AUTOMÁTICAMENTE
    if form.validate_on_submit():

        nombre = form.nombre.data
        correo = form.correo.data

        print("\n===== DATOS RECIBIDOS =====")
        print("Nombre:", nombre)
        print("Correo:", correo)
        print("===========================")

        return f"""
        <h2>Registro exitoso</h2>
        <p>Nombre: {nombre}</p>
        <p>Correo: {correo}</p>
        <a href="/">Volver</a>
        """

    # Si es GET o falla validación
    return render_template('registro.html', form=form)


# ==========================================
# MANEJO DE ERROR CSRF
# ==========================================
# Si el token:
# - No existe
# - Es inválido
# - Fue manipulado
# Flask lanza error 400
# ==========================================

@app.errorhandler(400)
def csrf_error(error):
    return """
    <h2>Error CSRF detectado</h2>
    <p>El formulario no tiene token válido o fue modificado.</p>
    <a href="/">Volver</a>
    """, 400


# ==========================================
# EJECUCIÓN DE LA APLICACIÓN
# ==========================================

if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
