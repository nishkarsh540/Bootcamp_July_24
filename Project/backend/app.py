from flask import Flask, jsonify,make_response
from flask_restful import Api, Resource,reqparse
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash,check_password_hash
from model import db,User

app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'grocery'


db.init_app(app)
CORS(app,origins='*')
jwt = JWTManager(app)
api = Api(app)


if __name__ =="__main__":
    app.run(debug=True)