# importing the db from app that is in __init__.py
# this acts as main while accessing in app

# current dir import app that is __init__.py
from . import app
from app import db
# impoting the instance that created in init py
from app import bcrypt

# define a model in database
# creating a table in database
class Task(db.Model):
    id = db.Column(db.Integer(),primary_key=True) # this is the id and name used in database schema
    name = db.Column(db.String(200), nullable=False, unique=True)
    duedate = db.Column(db.String(10), nullable=True)
    description = db.Column(db.String(400),nullable=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Do {self.name}'
    
# creating the user table
class User(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email_address = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable = False)
    user_task = db.relationship('Task', backref='owned_user', lazy=True)

    # adding the getter and setter for hased password
    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

# Insert dummy data into the database
with app.app_context():
    db.create_all()
    
    if not Task.query.first():
        dummy_Task = [
            Task(name='Task 1', duedate='2023-10-01', description='Description for task 1',owner=1),
            Task(name='Task 2', duedate='2023-10-02', description='Description for task 2',owner=1),
            Task(name='Task 3', duedate='2023-10-03', description='Description for task 3',owner=1)
        ]
        db.session.bulk_save_objects(dummy_Task)
        db.session.commit()

    if not User.query.first():
        master_user = [
            User(username = 'admin', email_address = 'admin@gmail.com', password_hash = "admin"),
            User(username = 'inovaix', email_address = 'inovaix@gmail.com', password_hash = "inovaix")
        ]
        db.session.bulk_save_objects(master_user)
        db.session.commit()

        db.session.close()