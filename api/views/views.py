import os
import hashlib
from flask_restful import Resource
from flask import request, send_from_directory
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.utils import secure_filename
# from datetime import datetime
# from celery import Celery
from ..models import db, User, Task, UserSchema, TaskSchema


ALLOWED_EXTENSIONS = {'zip', '7z', 'tar.gz', 'tar.bz2'}
UPLOAD_FOLDER = '../files'

user_schema = UserSchema()
task_schema = TaskSchema()


class ViewSignUp(Resource):
    def post(self):
        password1 = request.json['password1']
        password2 = request.json['password2']
        if (password1 != password2):
            return {'mensaje': 'La contraseña no coinciden'}

        encrypted_password = hashlib.md5(
            request.json["password1"].encode('utf-8')
        ).hexdigest()

        new_user = User(
            username=request.json['username'],
            password=encrypted_password,
            email=request.json['email'],
        )
        db.session.add(new_user)
        db.session.commit()
        return {'mensaje': 'Usuario creado correctamente'}

    def put(self, id_user):
        user = User.query.get_or_404(id_user)
        user.password = request.json.get('password', user.password)
        db.session.commit()
        return user_schema.dump(user)

    def delete(self, id_user):
        user = User.query.get_or_404(id_user)
        db.session.delete(user)
        db.session.commit()
        return '', 204


class ViewLogIn(Resource):
    def post(self):
        username = request.json['username']
        password = request.json['password']
        encrypted_password = hashlib.md5(
            password.encode('utf-8')).hexdigest()
        user = User.query.filter_by(
            username=username, password=encrypted_password).all()
        if user:
            # args = (name, datetime.utcnow())
            # registrar_log.apply_async(args=args, queue='logs')
            access_token = create_access_token(
                identity=request.json['username'])
            return {'mensaje': 'Inicio de sesión exitoso', 'accessToken': access_token}, 200
        else:
            return {'mensaje': 'Credenciales incorrectas'}, 401


class ViewTasks(Resource):
    @jwt_required()
    def post(self):
        if 'file' not in request.files:
            return {'mensaje': 'Archivo no encontrado'}

        file = request.files['file']
        if file.filename == '':
            return {'mensaje': 'No archivo seleccionado'}

        filename = file.filename or ''
        file_format = filename.rsplit('.', 1)[1].lower()
        if file and allowed_file(file_format):
            secured_filename = secure_filename(filename)
            file.save(os.path.join(UPLOAD_FOLDER, secured_filename))

            user = User.query.filter_by(username=get_jwt_identity()).first()
            new_task = Task(
                filename=secured_filename,
                format=file_format,
                new_format=request.form['newFormat'],
                user_id=user.id
            )
            db.session.add(new_task)
            db.session.commit()
            return {'mensaje': 'Archivo cargado'}

    @jwt_required()
    def get(self):
        tasks = Task.query.all()
        return [task_schema.dump(task) for task in tasks]

class ViewTask(Resource):
    @jwt_required()
    def get(self, id_task):
        return task_schema.dump(Task.query.get_or_404(id_task))

    @jwt_required()
    def delete(self, id_task):
        task = Task.query.get_or_404(id_task)
        db.session.delete(task)
        db.session.commit()
        return {'mensaje': 'Tarea eliminada correactamente'}, 204


def allowed_file(file_format):
    return file_format in ALLOWED_EXTENSIONS


class ViewFiles(Resource):
    @jwt_required()
    def get(self, filename):
        return send_from_directory(UPLOAD_FOLDER, filename)
