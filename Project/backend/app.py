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

class SignupResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username',type=str,required=True)
        parser.add_argument('email',type=str,required=True)
        parser.add_argument('password',type=str)
        parser.add_argument('role',type=str,default='user')

        args = parser.parse_args()

        if User.query.filter_by(username=args['username']).first():
            return{"message":"username already exists"},400
        
        hashed_password = generate_password_hash(args['password'])

        new_user = User(username=args['username'],email=args['email'],password = hashed_password,role=args['role'])

        db.session.add(new_user)
        db.session.commit()

        return {"message":"User Created Successfully"},200

api.add_resource(SignupResource,'/api/signup')

if __name__ =="__main__":
    app.run(debug=True)