# Imporing the  required packakage
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# settign a app / Initilaze an app
app = Flask(__name__)

# confing the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mystore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'inovaix'

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
