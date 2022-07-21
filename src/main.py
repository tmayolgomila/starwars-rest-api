"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, Characters, Planets

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def handle_hello():
    users = Users.query.all()
    listUsers = list(map(lambda obj: obj.serialize(),users))
    response_body = {
        "result":listUsers
    }
    return jsonify(response_body), 200

@app.route('/characters', methods=['GET'])
def handle_characters():
    characters = Characters.query.all()
    listCharacters = list(map(lambda obj:obj.serialize(),characters))
    response_body={
        "result":listCharacters
    }
    return jsonify(response_body), 200
    
@app.route('/characters/<int:id>', methods = ['GET'])
def handle_single_character():
    single_characters = Characters.query.get(id)
    characters = single_characters.serialize()
    response_body = {
        "result":characters
    }
    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def handle_planets():
    planets = Planets.query.all()
    listPlanets = list(map(lambda obj:obj.serialize(),planets))
    response_body={
        "result":listPlanets
    }
    return jsonify(response_body), 200
    
@app.route('/planets/<int:id>', methods = ['GET'])
def handle_single_planet():
    single_planets = Planets.query.get(id)
    planets = single_planets.serialize()
    response_body = {
        "result":planets
    }
    return jsonify(response_body), 200

@app.route('/users/favorites', methods = ['GET'])
def fav_users(users_id):
    favorito_character=Users.query.filter_by(id=users_id).first().characters
    favorito_planet= Users.query.filter_by(id=users_id).first().planets
    lista_favoritos=[]
    for i in favorito_character:
        lista_favoritos.append(i.serialize())
    for x in favorito_planet:
        lista_favoritos.append(x.serialize())
    return jsonify(lista_favoritos), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_fav_planet(planets_id):
    planeta=Planets.query.get(planets_id)
    usuario=Users.query.get(1)
    usuario.planets.append(planeta)
    db.session.commit()
    return jsonify({"succes":"planeta agregado"}), 200



@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_fav_character(characters_id):
    personaje=Characters.query.get(characters_id)
    usuario=Users.query.get(1)
    usuario.characters.append(personaje)
    db.session.commit()
    return jsonify({"succes":"personaje agregado"}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(planets_id):
    planeta= Planets.query.get(planets_id)
    usuario= Users.query.get(1)
    usuario.planets.remove(planeta)
    db.session.commit()
    return jsonify({"succes":"planeta eliminado"}), 200

@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_fav_chracter(characters_id):
    personaje= Characters.query.get(characters_id)
    usuario= Users.query.get(1)
    usuario.planets.remove(planeta)
    db.session.commit()
    return jsonify({"succes":"planeta eliminado"}), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)