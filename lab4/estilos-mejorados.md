# templates/login.html

<pre>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Login Seguro / Laboratorio</title>

    <!-- Tailwind CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
</head>

<body class="bg-gray-900 flex items-center justify-center h-screen">

    <div class="bg-gray-800 p-10 rounded-2xl shadow-2xl w-full max-w-md">

        <h1 class="text-3xl font-bold text-center text-cyan-400 mb-6">
            🔐 Login del Sistema
        </h1>

        <form method="POST" class="space-y-5">

            <input type="text"
                   name="usuario"
                   placeholder="Usuario"
                   class="w-full p-3 rounded-lg bg-gray-700 text-white focus:ring-2 focus:ring-cyan-400 outline-none">

            <input type="password"
                   name="password"
                   placeholder="Password"
                   class="w-full p-3 rounded-lg bg-gray-700 text-white focus:ring-2 focus:ring-cyan-400 outline-none">

            <button type="submit"
                    class="w-full bg-cyan-500 hover:bg-cyan-600 text-black font-bold p-3 rounded-lg transition">
                Ingresar
            </button>

        </form>

        <p class="text-gray-400 text-sm text-center mt-4">
            Laboratorio de seguridad web
        </p>

    </div>

</body>
</html>
 
</pre>

# templates/sugerencias.html
<pre>

  <!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Buzón de Sugerencias</title>

    <script src="https://cdn.tailwindcss.com"></script>
</head>

<body class="bg-gray-900 text-white">

    <!-- HEADER -->
    <div class="bg-gray-800 p-6 shadow-md flex justify-between items-center">
        <h1 class="text-2xl font-bold text-cyan-400">
            💬 Buzón de Sugerencias
        </h1>

        <span class="text-gray-300">
            Usuario activo
        </span>
    </div>

    <!-- CONTENIDO -->
    <div class="max-w-4xl mx-auto p-6">

        <!-- FORMULARIO -->
        <form method="POST" class="bg-gray-800 p-6 rounded-2xl shadow-lg mb-6">

            <h2 class="text-xl font-semibold mb-4 text-cyan-300">
                Nueva sugerencia
            </h2>

            <input type="text"
                   name="mensaje"
                   placeholder="Escribe tu sugerencia..."
                   class="w-full p-3 rounded-lg bg-gray-700 text-white focus:ring-2 focus:ring-cyan-400 outline-none mb-4">

            <button class="bg-green-500 hover:bg-green-600 text-black font-bold px-6 py-2 rounded-lg">
                Enviar
            </button>

        </form>

        <!-- LISTA DE MENSAJES -->
        <div class="space-y-4">

            {% for m in datos %}

            <div class="bg-gray-800 p-4 rounded-xl border border-gray-700 hover:border-cyan-400 transition">

                <p class="text-gray-200">
                    {{ m[0] }}
                </p>

            </div>

            {% endfor %}

        </div>

    </div>

</body>
</html>
  
</pre>
