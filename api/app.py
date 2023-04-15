from api import create_app
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .models import db
from .views import ViewSignIn, ViewLogIn

# import redis

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)

class ViewHelloWorld(Resource):
    def get(self):
        return 'Hello world!'

# Routes
api.add_resource(ViewHelloWorld, '/')
api.add_resource(ViewSignIn, '/signin')
api.add_resource(ViewLogIn, '/login')


jwt = JWTManager(app)
