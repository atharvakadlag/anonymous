from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from anonymous import db, login_manager

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

    def get_reset_token(self, expires_sec=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        token = s.dumps({'user_id': self.id}).decode('utf-8')
        return token

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Users.query.get(user_id)

    def __repr__(self):
        return f'User({self.name}, {self.username}, {self.email})'
    
class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receiver = db.Column(db.String(300), nullable=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), default=1)

    def __repr__(self):
        return f'Message({self.receiver}, {self.content[:120]})'
    