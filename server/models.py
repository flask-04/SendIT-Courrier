from sqlalchemy_serializer import SerializerMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re
from flask_bcrypt import Bcrypt 
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime 

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model,SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False, unique = True)
    email = db.Column(db.String)
    hashed_password = db.Column(db.String, nullable = False)
    parcels = db.relationship('Parcel', backref='user')
    notifications = db.relationship('UserNotification', backref='user', foreign_keys='UserNotification.user_id')

    # validates email
    @validates('email')
    def validate_email(self, key, email):
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'    
        if not re.match(email_pattern, email):
            raise ValueError('Invalid email format')
        
        return email
        
     # Password getter and setter methods
    @hybrid_property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, plain_text_password):
        self.hashed_password = bcrypt.generate_password_hash(
            plain_text_password.encode('utf-8')).decode('utf-8')

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.hashed_password, attempted_password.encode('utf-8'))
        
    def serialize(self):
        return{
            'id':self.id,
            'username':self.username,
            'email':self.email,
        }
    
class Parcel(db.Model, SerializerMixin):
    __tablename__ = 'parcels'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    weight = db.Column(db.Integer)
    status = db.Column(db.String(255))
    created_at = db.Column(db.DateTime,server_default=db.func.now())

    def serialize(self):
        return{'user_id':self.user_id,
               'weight':self.weight,
               'status':self.status
               }
    

class Delivery(db.Model,SerializerMixin):
    __tablename__ = 'deliveries'
    id = db.Column(db.Integer, primary_key=True)
    parcel_id = db.Column(db.Integer, db.ForeignKey('parcels.id'))
    title = db.Column(db.String(255))
    body = db.Column(db.Text)
    status = db.Column(db.String(255))
    created_at = db.Column(db.DateTime,server_default=db.func.now())

    def serialize(self):
        return{'parcel_id':self.parcel_id,
               'title':self.title,
               'body':self.body,
               'status':self.status
               }

class Location(db.Model, SerializerMixin):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    delivery_id = db.Column(db.Integer, db.ForeignKey('deliveries.id'))
    location = db.Column(db.String(255))
    status = db.Column(db.String(255))
    created_at = db.Column(db.DateTime,server_default=db.func.now())

    def serialize(self):
        return{'delivery_id':self.delivery_id,
               'location':self.location,
               'status':self.status
               }

class UserNotification(db.Model , SerializerMixin):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    notification = db.Column(db.String(255))
    delivery_id = db.Column(db.Integer, db.ForeignKey('deliveries.id'))
    created_at = db.Column(db.DateTime,server_default=db.func.now())

    def serialize(self):
        return{'user_id':self.user_id,
               'notification': self.notification,
               'delivery_id' : self.delivery_id
               }