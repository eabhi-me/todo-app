# Imporing the  required packakage
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import smtplib

#adding mail package
from flask_mail import Mail, Message

# seting the environment
from dotenv import load_dotenv
import os
load_dotenv()


# settign a app / Initilaze an app
app = Flask(__name__)

# confing the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mystore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# adding mail cilent


app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
)
mail = Mail(app)

# Starting the database
db = SQLAlchemy(app)

# an insatnace for encryption and hashing
bcrypt = Bcrypt(app)

# intatiate an login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# importing the  routes
from app import routes
