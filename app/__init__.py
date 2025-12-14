from flask import Flask
from app.db import init_db
import os

def create_app():
    app = Flask(__name__)

    database_url = os.getenv("DATABASE_URL")
    if database_url:
        init_db(database_url)

    from app.db import engine, Base
    from app.models import URL, Click
    Base.metadata.create_all(engine)
        
    from app.routes import health_bp, urls_bp
    app.register_blueprint(health_bp)
    app.register_blueprint(urls_bp)
    
    return app

