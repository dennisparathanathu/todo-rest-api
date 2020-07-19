import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UserModel(db.Model):
    """
    User Model
    """

    # table name
    __tablename__ = 'todousers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)
    todos = db.relationship('TodosModel', backref='todousers', lazy=True)

    # class constructor
    def __init__(self, name, email, password):
        """
        Class constructor
        """
        self.name = name
        self.email = email
        self.password = password


class TodosModel(db.Model):
    """
    Blogpost Model
    """

    __tablename__ = 'todolists'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    contents = db.Column(db.Text, nullable=False)
    created_dt = db.Column(db.DateTime)
    tododate = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('todousers.id'), nullable=False)

    def __init__(self, title, contents, created_dt, tododate, user_id):
        self.title = title
        self.contents = contents
        self.created_dt = created_dt
        self.tododate = tododate
        self.user_id = user_id
