from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class TodoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'completed': self.completed
        }

# @app.route('/')
# def home():
# #     return "ankit"
@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todos(todo_id):
    todos = TodoItem.query.all()
    return jsonify([t.to_dict() for t in todos])

@app.route('/todos', methods=['POST'])
def create_todo():
    todo_data = request.json
    todo = TodoItem(title=todo_data['title'], completed=todo_data.get('completed', False))
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict())

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = TodoItem.query.get_or_404(todo_id)
    todo_data = request.json
    todo.title = todo_data.get('title', todo.title)
    todo.completed = todo_data.get('completed', todo.completed)
    db.session.commit()
    return jsonify(todo.to_dict())


@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = TodoItem.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return '', 204


@app.route('/todos/<int:todo_id>',methods = ['PUT'])
def task_completed(todo_id):
    todo = TodoItem.query.get_or_404(todo_id)
    todo_data = request.json
    todo.completed = todo_data.get('completed', todo.completed)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)


