from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("registro.html")

@app.route("/guardar", methods=["POST"])
def guardar():

    nombre = request.form["nombre"]
    correo = request.form["correo"]

    print("Usuario registrado")
    print(nombre)
    print(correo)

    return "Registro exitoso"

if __name__ == "__main__":
    app.run(debug=True)
