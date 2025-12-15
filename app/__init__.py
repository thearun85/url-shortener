from flask import Flask
from app.db import init_db
from app.redis_client import init_redis
import os

def create_app():
    app = Flask(__name__)

    database_url = os.getenv("DATABASE_URL")
    if database_url:
        init_db(database_url)
    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        init_redis(redis_url)
        
    from app.routes import health_bp, urls_bp, redirect_bp
    app.register_blueprint(health_bp)
    app.register_blueprint(urls_bp)
    app.register_blueprint(redirect_bp)
    
    return app

