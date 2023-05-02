import hashlib
from typing import Callable

from flask import redirect, render_template, request, session, url_for

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
# ------------------VIEW DE LOGIN-------------------------
    @app.route("/", methods=["GET", "POST"])
    def login():
        if request.method == "GET":
            return render_template("login.html")
        
        if request.method == "POST":
            usuario = request.form["usuario"]
            contrasena = request.form["contrasena"]
            session['usuario'] = usuario
            return redirect(url_for('inicio'))
        
    # ------------------Cerrar Sesion------------------------
    @app.route("/logout", methods=["GET", "POST"])
    def logout():
        session.clear()
        return render_template("login.html")
    
    # ------------------VIEW DE Inicio-------------------------

    @app.route("/inicio", methods=["GET", "POST"])
    def inicio():
        return render_template("index.html")


        """
        # Verificar si el usuario ha iniciado sesión
        if 'usuario' not in session:
            return redirect(url_for('login'))

        # Si el usuario ha iniciado sesión, mostrar la vista de inicio
        return render_template("index.html")
        """
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
            return redirect("/")

    # ------------------VIEW DE Toldos-------------------------
    
    
    @app.route("/toldo", methods=["GET", "POST"])
    def toldo():

        list_toldo = db_access["list_toldos"]
        toldos = list_toldo()
        return render_template("toldos.html", toldos=toldos)
    
    @app.route("/delete_toldo/<int:Toldo_id>", methods=["GET", "POST"])
    def delete_toldo(Toldo_id: int):
        if request.method == "GET":
            read_toldo = db_access["read_toldo"]
            toldo = read_toldo(Toldo_id)
            return render_template("delete_toldo.html", toldo=toldo)

        if request.method == "POST":
            delete_toldo= db_access["delete_toldo"]
            delete_toldo(
                Toldo_id=Toldo_id
            )
            return redirect("/toldo")
    
    @app.route("/create_toldo", methods=["GET", "POST"])
    def create_toldo():
        if request.method == "GET":
            list_toldo = db_access["list_toldos"]
            toldos = list_toldo()

            return render_template("create_toldo.html", toldos=toldos)

        if request.method == "POST":
            create_toldo = db_access["create_toldo"]
            create_toldo(
                modelo=request.form["modelo"],
                tipo=request.form["tipo"],
                dimensiones=request.form["dimensiones"],
                imagen=request.form["imagen"]
            )
            return redirect("/toldo")
    
    @app.route("/update_toldo/<int:Toldo_id>", methods=["GET", "POST"])
    def updtae_toldo(Toldo_id: int):
        if request.method == "GET":
            read_toldo = db_access["read_toldo"]
            toldo = read_toldo(Toldo_id)
            return render_template("update_toldo.html", toldo=toldo)

        if request.method == "POST":
            update_toldo = db_access["update_toldo"]
            update_toldo(
                Toldo_id = Toldo_id,
                modelo=request.form["modelo"],
                tipo=request.form["tipo"],
                dimensiones=request.form["dimensiones"],
            )
            return redirect("/toldo")