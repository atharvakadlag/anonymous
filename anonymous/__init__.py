from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' 
login_manager.login_message_category = 'info' 
mail = Mail(app)

from anonymous import routes
from anonymous import models