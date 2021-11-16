from flask_sqlalchemy import SQLAlchemy
import os
import sys
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), unique=False, nullable=False)
    favorites  = db.relationship('Favorite', backref='user', uselist=True)
    
    def serialize(self):
        return {
            "user_name": self.user_name,
            "id": self.id
        }
    
    @classmethod
    def create(cls, bubulala):
        try:
            new_user = cls(**bubulala)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception as error:
            db.session.rollback()
            print(error)
            return None


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    url = db.Column(db.String(125), nullable=False) 
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint(
        'user_id',
        'url',
        name='fav_user'
    ),)

    def serialize(self):
        return {
            "user_id": self.user_id,
            "swapi_url": self.url,
            "url": "/detail/"+self.url.replace("https://www.swapi.tech/api/", ""),
            "id": self.id,
            "favName": self.name
        }
    
    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            return False
    

