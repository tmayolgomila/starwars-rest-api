from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

fav_characters = db.Table('favorite_character',
    db.Column('users_id', db.Integer, db.ForeignKey('users.id'),primary_key=True),
    db.Column('characters_id', db.Integer, db.ForeignKey('characters.id', primary_key=True))
    )
fav_planets = db.Table('favorite_planet',
    db.Column('users_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('planets_id', db.Integer, db.ForeignKey('planets.id'), primary_key=True)
    )
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250))
    characters = relationship('Characters', secondary=fav_characters)
    planets = relationship('Planets', secondary=fav_planets)
    def __repr__(self):
        return '<Users %r>' % self.username
    def serialize(self):
        return{
            "id":self.id,
            "username":self.username,
            "name":self.name,
            "last_name":self.last_name,
            "email":self.email,
            "rel_FavCharacters":self.rel_FavCharacters
        }
class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<Characters %r>' % self.name
    def serialize(self):
        return{
            "id":self.id,
            "name":self.name
        }
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.name
    def serialize(self):
        return{
            "id":self.id,
            "name":self.name
        }