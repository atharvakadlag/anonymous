from anonymous import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return Users.query.get(id)

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=True)
    username = db.Column(db.String(70), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    messages = db.relationship('Messages', backref='sender', lazy=True)

    def __repr__(self):
        return f'User({self.name}, {self.username}, {self.email})'
    
class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receiver = db.Column(db.String(300), nullable=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), default=1)

    def __repr__(self):
        return f'Message({self.receiver}, {self.content[:120]})'
    