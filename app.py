from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    is_complete = db.Column(db.Boolean)

@app.route('/')
def index():
    todo_list = Todo.query.all()
    print(todo_list)
    return render_template('index.html', todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, is_complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.is_complete = not todo.is_complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    db.create_all()

    new_todo = Todo(title="todo 1", is_complete=False)
    db.session.add(new_todo)
    db.session.commit()

    app.run(debug=True)