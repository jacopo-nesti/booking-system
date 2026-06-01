from flask import Flask
from app.database import init_db
from app.routes import main

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'

    app.register_blueprint(main)
    
    return app