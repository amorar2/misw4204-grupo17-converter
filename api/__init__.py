import os
from flask import Flask

db_uri = os.environ.get('DATABASE_URL')
# Set a default value if the environment variable is not defined
if not db_uri:
    db_uri = 'postgresql://postgres:postgres@db:5432/converter'

def create_app(config_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    # app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/converter"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['JWT_SECRET_KEY'] = 'grupo17-converter-key'
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    return app
