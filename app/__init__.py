from flask import Flask
from app.database import init_db
from app.routes import main
import os
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

    app.register_blueprint(main)
    
    return app