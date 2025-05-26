from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "your_secret_key"

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)


with app.app_context():
    db.create_all()


# ✅ Step 1: Index Route - Display Tasks
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)


# ✅ Step 2: Improved Add Task Route (Includes Validation)
@app.route('/add', methods=['POST'])
def add_task():
    task_name = request.form['task'].strip()  # Remove unnecessary spaces
    if not task_name:
        flash("Task name cannot be empty!", "danger")  # Show error message
    elif Task.query.filter_by(name=task_name).first():
        flash("Task already exists!", "warning")  # Prevent duplicate entries
    else:
        new_task = Task(name=task_name)
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully!", "success")  # Success message

    return redirect(url_for('index'))


# ✅ Step 3: Delete Task Route
@app.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
        flash("Task deleted!", "danger")
    return redirect(url_for('index'))


# ✅ Step 4: Toggle Task Completion
@app.route('/toggle/<int:id>')
def toggle_task(id):
    task = Task.query.get(id)
    if task:
        task.completed = not task.completed
        db.session.commit()
        flash(f"Task '{task.name}' marked as {'Completed' if task.completed else 'Pending'}!", "info")
    return redirect(url_for('index'))


# ✅ Step 5: Task Filtering (Show Completed or Pending Tasks)
@app.route('/filter/<status>')
def filter_tasks(status):
    if status == "completed":
        tasks = Task.query.filter_by(completed=True).all()
    else:
        tasks = Task.query.filter_by(completed=False).all()
    return render_template('index.html', tasks=tasks)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

