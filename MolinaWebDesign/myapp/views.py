import hashlib
from typing import Callable

from flask import redirect, render_template, request

# init_views inicializa la clase de las vistas
# app es un objeto flask creado en app.py (en app.py: app = Flask(__name__)
# db_access es el objeto que devuelve init_db para gestionar la base de datos (en app.py: db_access = init_db(app))
# ambos pasan como parámetros a init_views

# def validate_password(password: str, hashed_password: str) -> bool:
# return hash_password(password) == hashed_password

# ------------------FUNCION DE HASH DE LA PASSWORD-------------------------


def hash_password(password: str) -> str:
    salt = "mysecretsalt"  # puedes usar un valor diferente aquí
    return hashlib.sha256((password + salt).encode()).hexdigest()
# ----------------------------------------------------------------------------


def init_views(app, db_access: dict[str, Callable]):
    # definición de las acciones a realizar para lanzar cada vista
    # nótese que el código de "/" no pregunta si se ha hecho una petición, así que deberá ejecutarse al inicializar
    # en el caso de los demás tienen sentencias IF para que el código se ejecute solo si haya una petición

    @app.route("/", methods=["GET", "POST"])
    def index():

        return render_template("login.html")

    # ------------------VIEW DE LOGIN-------------------------

    @app.route("/login", methods=["GET", "POST"])
    def login():
        return render_template("index.html")

    # ------------------VIEW DE REGISTRO-------------------------

    @app.route("/create_usuario", methods=["GET", "POST"])
    def create_usuario():
        if request.method == "GET":
            return render_template("registro.html")

        if request.method == "POST":
            create_usuario = db_access["create_usuario"]
            contrasena_hash = hash_password(request.form["contrasena"])
            create_usuario(
                usuario=request.form["usuario"],
                correo=request.form["correo"],
                contrasena=contrasena_hash,
                rol=""
            )
            return redirect("/login")

    # ------------------VIEW DE Inicio-------------------------

    @app.route("/inicio", methods=["GET", "POST"])
    def inicio():
        if request.method == "POST":
            # Obtener el usuario de la base de datos
            get_user = db_access["get_user"]
            user = get_user(usuario=request.form["usuario"])

            # Verificar si el usuario existe y si la contraseña coincide
            if user and user["contrasena"] == hash_password(request.form["contrasena"]):
                # Redirigir al usuario a la página correspondiente
                if user["rol"] == "admin":
                    return redirect("/admin")
                else:
                    return redirect("/usuario")
            else:
                # Informar al usuario de que la autenticación ha fallado
                return render_template("inicio.html", error="Credenciales incorrectas")

    # Si la petición es GET, simplemente renderiza la plantilla
    return render_template("inicio.html")
