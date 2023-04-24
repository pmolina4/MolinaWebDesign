from typing import Callable

from flask import redirect, render_template, request

# init_views inicializa la clase de las vistas
# app es un objeto flask creado en app.py (en app.py: app = Flask(__name__)
# db_access es el objeto que devuelve init_db para gestionar la base de datos (en app.py: db_access = init_db(app))
# ambos pasan como parámetros a init_views


def init_views(app, db_access: dict[str, Callable]):
    # definición de las acciones a realizar para lanzar cada vista
    # nótese que el código de "/" no pregunta si se ha hecho una petición, así que deberá ejecutarse al inicializar
    # en el caso de los demás tienen sentencias IF para que el código se ejecute solo si haya una petición

    @app.route("/", methods=["GET", "POST"])
    def index():

        return render_template("index.html")

