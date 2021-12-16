from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_app import db, login_manager
from flask_login import UserMixin


# Define a decorator function which takes argument as user_id and return the user for that ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create a class for users, Inheriting from dp.model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(25), nullable = False)
    email = db.Column(db.String(125), unique = True, nullable = False)
    image_file = db.Column(db.String(25), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)
    posts = db.relationship('Post', backref = 'author', lazy = True)

    # define a method to get a token for reseting the password
    def get_reset_token(self, expires_sec=600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    # define a method to verify the token
    @staticmethod # basically telling to the python, this method is not accepting 'self' as an argument
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        # try to get the user_id from the token
        try:
            user_id = s.loads(token)['user_id']
        except: # if we get an exception 
            return None # when token is invalid or expired
        return User.query.get(user_id) # if we don't get an exception
        


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# Create a Post class to hold our posts, Inheriting from dp.model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date}')"