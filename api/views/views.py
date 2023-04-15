from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, create_access_token
# from datetime import datetime
# from celery import Celery
from ..models import db, User, UserSchema

user_shema = UserSchema()

class ViewSignIn(Resource):
    def post(self):
        new_user = User(
            username=request.json['username'],
            password=request.json['password'],
            email=request.json['email'],
        )
        access_token = create_access_token(identity=request.json['email'])
        db.session.add(new_user)
        db.session.commit()
        return {'mensaje': 'Usuario creado correctamente', 'accessToken': access_token}

    def put(self, id_user):
        user = User.query.get_or_404(id_user)
        user.password = request.json.get('password', user.password)
        db.session.commit()
        return user_shema.dump(user)

    def delete(self, id_user):
        user = User.query.get_or_404(id_user)
        db.session.delete(user)
        db.session.commit()
        return '', 204

class ViewLogIn(Resource):
    def post(self):
        # username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        user = User.query.filter_by(
            email=email, password=password).all()
        if user:
            # args = (name, datetime.utcnow())
            # registrar_log.apply_async(args=args, queue='logs')
            return {'mensaje': 'Inicio de sesión exitoso'}, 200
        else:
            return {'mensaje': 'Usuario no encontrado'}, 401

