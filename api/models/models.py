import enum
import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()


class EnumTipoUsuario(enum.Enum):
    PROCESSED: str = 'PROCESSED'
    UPLOADED: str = 'UPLOADED'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    tasks = db.relationship('Task', back_populates='user')


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(500))
    format = db.Column(db.String(50))
    new_format = db.Column(db.String(50))
    status = db.Column(db.Enum(EnumTipoUsuario),
                       default=EnumTipoUsuario.UPLOADED)
    crated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='tasks')


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True


class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_relationships = True
        load_instance = True
