from typing import Callable  # para agregar anotaciones a las clases

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Sequence


def init_db(app) -> dict[str, Callable]:
    db = SQLAlchemy(app)

    # esta clase gestionará la tabla, hay que pasarle la clase base de
    # todos los modelos de Flask alchemy que es db.Model
    class Usuario(db.Model):

        __tablename__ = "Usuario"  # Nombre de la tabla que se crea

        # declarar campos de la tabla "Equipo"
        Usuario_id = db.Column("usuario_id", db.Integer, Sequence(
            'usuario_id_seq'),  primary_key=True)
        Usuario = db.Column(db.String(20))
        Correo = db.Column(db.String(50))
        Contrasena = db.Column(db.String(50))
        Rol = db.Column(db.String(10))

        def __str__(self):
            return f"[{self.usuario}] {self.correo} {self.contrasena} {self.rol}"


   # ------------- FUNCIONES DE USUARIO -----------
    def create_usuario(usuario: str, correo: str, contrasena: str, rol: str):
        usuario = Usuario(
            Usuario=usuario, Correo=correo, Contrasena=contrasena, Rol=rol
        )
        db.session.add(usuario)
        db.session.commit()

    # create_all es un método de Flask-alchemy que crea la tabla con sus campos
    db.create_all()

    return {
        # estos alias serán usados para llamar a los métodos de la clase, por ejemplo db_access["create"]
        # invoca al método create_contact
        "create_usuario": create_usuario

    }
