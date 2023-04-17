from flask import Flask


def create_app(config_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@db:5432/converter"
    # app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/converter"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['JWT_SECRET_KEY'] = 'grupo17-converter-key'
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    return app
