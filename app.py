from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
Scss(app)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class Mytasks(db.Model):    #database model
    id = db.Column(db.Integer, primary_key=True)
    contents = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Task {self.id}"


@app.route('/', methods=["POST", 'GET'])
def index():
    # add a task
    if request.method == 'POST':    
        current_task = request.form['content']
        new_task = Mytasks(contents = current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
    #see all tasks
    else:
        tasks = Mytasks.query.order_by(Mytasks.created).all()
        return render_template('index.html', tasks=tasks)

    # delete a task

@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = Mytasks.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"ERROR:{e}"
    

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id:int):
    task = Mytasks.query.get_or_404(id)
    if request.method == 'POST':
        task.contents = request.form['content']   # updating the task
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"ERROR:{e}"
        
    else:
        return render_template('edit.html', task=task)

if __name__  == '__main__':
        
    with app.app_context():
        db.create_all()

    app.run(debug=True)