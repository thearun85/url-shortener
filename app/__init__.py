from flask import Flask, g
from app.db import init_db
import os

def create_app():
    app = Flask(__name__)

    database_url = os.getenv("DATABASE_URL")
    if database_url:
        init_db(database_url)
        from app.db import Base, engine
        from app import models
        Base.metadata.create_all(engine)

        
    from app.routes import health_bp
    app.register_blueprint(health_bp)

    return app
