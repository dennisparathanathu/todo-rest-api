from flask import Flask, jsonify, request, make_response
from .models import db, UserModel, TodosModel
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
from .auth import Auth



def create_app(env_name):
    """
    Create app
    """

    # app initiliazation
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:password@localhost:5432/todore'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    @app.route('/', methods=['GET'])
    def index():

        return 'todo REST api with jwt '

    @app.route('/register', methods=['GET', 'POST'])
    def register_user():
        data = request.get_json()

        hashed_password = generate_password_hash(data['password'], method='sha256')

        new_user = UserModel(name=data['name'], email=data['email'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'registered successfully'})

    @app.route('/login', methods=['GET', 'POST'])
    def login_user():

        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

        user = UserModel.query.filter_by(name=auth.username).first()

        if check_password_hash(user.password, auth.password):
            token = jwt.encode(
                {'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                os.getenv('JWT_SECRET_KEY'))
            return jsonify({'token': token.decode('UTF-8')})

        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    @app.route('/todo', methods=['POST', 'GET'])
    @Auth.token_required
    def create_todo(current_user):

        data = request.get_json(force=True)
        print(data)

        
        new_todos = TodosModel(title=data['title'], contents=data['contents'], created_dt=datetime.datetime.utcnow(), tododate=data['tododate'], user_id=current_user.id)
        db.session.add(new_todos)
        db.session.commit()

        return jsonify({'message': 'new todo created'})

    @app.route('/view-todo', methods=['POST', 'GET'])
    @Auth.token_required
    def get_todos(current_user):

        todos = TodosModel.query.filter_by(user_id=current_user.id).all()

        output = []
        for todo in todos:
            todo_data = {}
            todo_data['title'] = todo.title
            todo_data['contents'] = todo.contents
            todo_data['created_dt'] = todo.created_dt
            todo_data['tododate'] = todo.tododate
            output.append(todo_data)

        return jsonify({'list_of_todos': output})

    @app.route('/delete-todo/<todo_id>', methods=['DELETE'])
    @Auth.token_required
    def delete_author(current_user, todo_id):
        todo = TodosModel.query.filter_by(id=todo_id, user_id=current_user.id).first()
        if not todo:
            return jsonify({'message': 'todo does not exist'})

        db.session.delete(todo)
        db.session.commit()

        return jsonify({'message': 'todo deleted'})

    return app
