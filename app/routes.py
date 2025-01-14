from flask import render_template, redirect, request, url_for, jsonify,flash
from app import app # __int__import
from app import db 
from app.models import *
from app.forms import RegisterForm, LoginForm
from flask_bcrypt import generate_password_hash
from flask_login import login_user, logout_user, current_user, login_required


# routing
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    owner= current_user.id
    tasks = Task.query.filter_by(owner=owner)
    return render_template('dashboard.html', tasks=tasks)

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
        login_user(new_user)
        return redirect(url_for('dashboard'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'The error found: {err_msg}','danger')

    return render_template('register.html', form = form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email_address = form.email_address.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password = form.password.data):
            login_user(attempted_user)
            flash(f'Success! You have loged in as {attempted_user.email_address}', category='info')
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect Email address or password', category='danger')
    return render_template('login.html', form=form)
    
@app.route('/logout')
def logout():
    logout_user()
    flash('You have been Logout',category='info')
    return redirect(url_for('login'))


@app.route('/add',methods=['GET','POST'])
# adding so that only login user can add and delete
@login_required
def add():
    if request.method =='POST':
        name = request.form['name']
        duedate = request.form['duedate']
        description = request.form['description']
        owner = current_user.id  # Ensure the owner is set to the current logged-in user
        new_task = Task(name=name, duedate=duedate, description=description, owner=owner)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return redirect(url_for('dashboard'))

@app.route('/delete/<int:id>', methods=['DELETE','GET'])
@login_required
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
        return redirect(url_for('dashboard'))
    
@app.route('/search', methods =['GET','POST'])
@login_required
def serach_by_key():
    if request.method =='POST':
        keyword = request.form['keyword']
        results = Task.query.filter(Task.name.like(f"%{keyword}%")).all()
        owner = current_user.id
        results = Task.query.filter(Task.name.like(f"%{keyword}%"), Task.owner == owner).all()
        return render_template('search_result.html',results=results,keyword=keyword)
    return redirect(url_for('dashboard'))