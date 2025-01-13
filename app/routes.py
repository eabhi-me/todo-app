from flask import render_template, redirect, request, url_for, jsonify
from app import app # __int__import
from app import db 
from app.models import *
from app.forms import RegisterForm, LoginForm
from flask_bcrypt import generate_password_hash


# routing
@app.route('/')
def home():
    tasks = Task.query.filter_by(owner=1)
    return render_template('index.html', tasks=tasks)

@app.route('/register', methods=['GET','POST'])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(
            username = form.username.data,
            email_address = form.email_address.data,
            password_hash = generate_password_hash(form.password1.data) # calling the function generate hash to hasinng
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            print(f'The error found: {err_msg}','danger')

    return render_template('register.html', form = form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)
    

@app.route('/add',methods=['GET','POST'])
def add():
    if request.method =='POST':
        name = request.form['name']
        duedate = request.form['duedate']
        description = request.form['description']
        owner = 1  # Ensure the owner is always set to id 1
        new_task = Task(name=name, duedate=duedate, description=description, owner=owner)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))
    return redirect(url_for('home'))

@app.route('/delete/<int:id>', methods=['DELETE','GET'])
def delete_task(id):
    if request.method=='DELETE':
        task = Task.query.get(id)
        if task:
            db.session.delete(task)
            db.session.commit()
            return jsonify({'message': 'Task deleted successfully'}), 200
        else:
            return jsonify({'message': 'Task not found'}), 404
    if request.method == 'GET':
        return redirect(url_for('home'))
    
@app.route('/search', methods =['GET','POST'])
def serach_by_key():
    if request.method =='POST':
        keyword = request.form['keyword']
        results = Task.query.filter(Task.name.like(f"%{keyword}%")).all()
        return render_template('search_result.html',results=results,keyword=keyword)
    return redirect(url_for('home'))