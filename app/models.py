from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime



class User(UserMixin,db.Model): 
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255), unique = True, index = True)
    email = db.Column(db.String(255),unique = True, index =True)
    role_id = db.Column(db.Integer,db.ForeignKey ('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))

    pitches = db.relationship('Pitches',backref = 'user',lazy ='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        
        return f'User {self.username}'

class Role(db.Model):
    __tablename__='roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy = 'dynamic')


    def __repr__(self):
        return f'User{self.name}'       


class Pitches (db.Model):
    '''
    Review class to define Review Objects
    '''
    __tablename__ = 'pitches'
    id = db.Column(db.Integer, primary_key =True)
    pitch = db.Column(db.String)
    posted = db.Column(db.DateTime,default = datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_pitches(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_pitch(cls,id):
        pitches = Pitches.query.filter_by(user_id = id).all()

        return pitches
        

class Coments(db.Model):
    __tablename__ = "coments"

    id = db.Column(db.Integer,primary_key =True)
    title = db.Column(db.String(250))
    comment = db.Column(db.String(1000))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))