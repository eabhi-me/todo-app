from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

# Creating an app as main starter
app = Flask(__name__)

# confing app with sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mystore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# creating dataabse
db = SQLAlchemy(app)

# define a model in database
# creating a table in database
class Task(db.Model):
    id = db.Column(db.Integer(),primary_key=True) # this is the id and name used in database schema
    name = db.Column(db.String(200), nullable=False, unique=True)
    duedate = db.Column(db.String(10), nullable=True)
    discription = db.Column(db.String(400),nullable=True)

    def __repr__(self):
        return f'Do {self.name}'
    
# Insert dummy data into the database
with app.app_context():
    db.create_all()
    
    if not Task.query.first():
        dummy_Task = [
            Task(name='Task 1', duedate='2023-10-01', discription='Description for task 1'),
            Task(name='Task 2', duedate='2023-10-02', discription='Description for task 2'),
            Task(name='Task 3', duedate='2023-10-03', discription='Description for task 3')
        ]
        db.session.bulk_save_objects(dummy_Task)
        db.session.commit()
        db.session.close()

# routing
@app.route('/')
def home():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add',methods=['GET','POST'])
def add():
    if request.method =='POST':
        name = request.form['name']
        duedate = request.form['duedate']
        discription = request.form['discription']
        new_task = Task(name=name, duedate=duedate, discription=discription)
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

# development server debug mmode on
if __name__ == '__main__':
    app.run(debug=True)
