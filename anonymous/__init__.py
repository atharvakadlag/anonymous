import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from anonymous.config import Config, ProductionConfig, DevelopmentConfig, StagingConfig

mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login' 
login_manager.login_message_category = 'info' 

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from anonymous.users.routes import users
    from anonymous.messages.routes import messages
    from anonymous.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(messages)
    app.register_blueprint(main)

    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    return app