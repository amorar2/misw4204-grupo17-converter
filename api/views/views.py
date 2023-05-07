import os
import hashlib
import datetime
import time
import calendar
from flask_restful import Resource
from flask import request, send_from_directory, current_app, send_file
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.utils import secure_filename
from io import BytesIO

from api.utils.files import delete_file_from_folder, allowed_files
from ..models import db, User, Task, UserSchema, TaskSchema, EnumStatusType
from ..tasks import register_convert_task


FILES_FOLDER = 'files'

user_schema = UserSchema()
task_schema = TaskSchema()


class ViewSignUp(Resource):
    def post(self):
        password1 = request.json['password1']
        password2 = request.json['password2']
        if (password1 != password2):
            return {'mensaje': 'La contraseña no coinciden'}

        encrypted_password = hashlib.md5(
            request.json['password1'].encode('utf-8')
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

        file_full_name = file.filename or ''
        file_props = file_full_name.split('.', 1)
        file_name = file_props[0].lower()
        file_format = file_props[1].lower()
        if file and allowed_files(file_format):
            user = User.query.filter_by(username=get_jwt_identity()).first()
            current_GMT = time.gmtime()
            time_stamp = calendar.timegm(current_GMT)
            custom_name = file_name + '_' + str(time_stamp)
            secured_file_name = secure_filename(
                custom_name + '.' + file_format)
            temp_path = os.path.join(FILES_FOLDER, secured_file_name)
            file.save(temp_path)

            # Guardar en bucket
            bucket = current_app.config['STORAGE_BUCKET_CLIENT']
            blob = bucket.blob(secured_file_name)
            blob.upload_from_filename(temp_path)

            if blob.exists():
                delete_file_from_folder(temp_path)
            else:
                print('Upload failed.')

            new_task = Task(
                file_name=file_name,
                custom_name=custom_name,
                format='.' + file_format,
                new_format=request.form['newFormat'],
                user_id=user.id
            )

            db.session.add(new_task)
            db.session.commit()

            register_convert_task.delay(str(new_task.id), file_name, str(
                time_stamp), new_task.format, new_task.new_format)

            return {'mensaje': 'Archivo cargado', 'new_task': task_schema.dump(new_task)}

    @jwt_required()
    def get(self):
        tasks = Task.query.all()
        return [task_schema.dump(task) for task in tasks]


class ViewTask(Resource):
    @jwt_required()
    def get(self, id_task):
        print(id_task)
        return task_schema.dump(Task.query.get_or_404(id_task))

    @jwt_required()
    def delete(self, id_task):
        task = Task.query.get_or_404(id_task)
        bucket = current_app.config['STORAGE_BUCKET_CLIENT']

        original_file = task.custom_name + task.format
        blob_original = bucket.blob(original_file)

        if blob_original.exists():
            blob_original.delete()
        else:
            print('File = ' + original_file + ' doesn\'t exist.')

        # if task.status == EnumStatusType.PROCESSED: #TODO
        converted_file = str(task.id) + '_' + task.file_name + task.new_format

        blob_converted = bucket.blob(converted_file)
        if blob_converted.exists():
            blob_converted.delete()
        else:
            print('File = ' + converted_file + ' doesn\'t exist.')

        db.session.delete(task)
        db.session.commit()
        return {'mensaje': 'Tarea eliminada correactamente'}, 200


class ViewFiles(Resource):
    # @jwt_required()
    def get(self, id_task):
        old = bool(request.args.get('old', False))
        task = Task.query.get_or_404(id_task)
        bucket = current_app.config['STORAGE_BUCKET_CLIENT']

        if old == True:
            original_file = task.custom_name + task.format
            blob = bucket.blob(original_file)
            file_contents = BytesIO()
            blob.download_to_file(file_contents)
            file_contents.seek(0)
            return send_file(
                file_contents,
                download_name=original_file,
                as_attachment=True
            )

        else:
            converted_file = str(task.id) + '_' + \
                task.file_name + task.new_format
            blob = bucket.blob(converted_file)
            file_contents = BytesIO()
            blob.download_to_file(file_contents)
            file_contents.seek(0)
            return send_file(
                file_contents,
                download_name=converted_file,
                as_attachment=True
            )
