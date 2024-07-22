from flask import Flask, jsonify,make_response
from flask_restful import Api, Resource,reqparse
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash,check_password_hash
from model import db,User,Category,Product
from flask_caching import Cache
import redis
from celery_config import celery

app =Flask(__name__)
redis_client = redis.Redis(host='localhost',port=6379,db=0)
cache = Cache(app,config={'CACHE_TYPE':'redis','CACHE_REDIS':redis_client})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'grocery'
celery.conf.update(app.config)


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
        if args['role'] == 'store-manager':
            new_user = User(username=args['username'],email=args['email'],password = hashed_password,role=args['role'],approved=False)
        else:
            new_user = User(username=args['username'],email=args['email'],password = hashed_password,role=args['role'],approved=True)

        db.session.add(new_user)
        db.session.commit()

        return {"message":"User Created Successfully"},200

class LoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username',type=str,required=True)
        parser.add_argument('password',type=str,required=True)
        args= parser.parse_args()
        
        user = User.query.filter_by(username=args['username']).first()
        if user and check_password_hash(user.password,args['password']):
            if user.approved == False:
                return {'message':'please wait for approval from the admin'},401
            access_token = create_access_token(identity=user.role)
            user_info={"id":user.id,
                       "username":user.username,
                       'role':user.role}
            return {'access_token':access_token,"user":user_info}, 200
        else:
            return {'message':'invalid username or password'},401

class UserInfo(Resource):
    @cache.cached(timeout=20)
    def get(self):
        users = User.query.all()
        user_info = [{
            "id":user.id,
            "username":user.username,
            "role":user.role
        } for user in users]
        return user_info

class CategoryResource(Resource):
    @jwt_required()
    def get(self):
        categories =Category.query.all()
        return jsonify([{
            'id':category.id,
            'name':category.name
        } for category in categories])

    def post(self):
        parser= reqparse.RequestParser()
        parser.add_argument('name',type=str,required=True)
        args=parser.parse_args()

        if Category.query.filter_by(name=args['name']).first():
            return {'message':'category already exists'},400
        new_category = Category(name=args['name'])
        db.session.add(new_category)
        db.session.commit()

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',type=int,required=True)
        parser.add_argument('name',type=str,required=True)
        args=parser.parse_args()

        category = Category.query.get(args['id'])
        if not category:
            return {'message':'category not found'},404
        
        category.name = args['name']
        db.session.commit()
        return {'message':'category updated successfully'},200
    
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',type=int,required=True)
        args=parser.parse_args()

        category = Category.query.get(args['id'])
        if not category:
            return {'message':'category not found'},404
        
        db.session.delete(category)
        db.session.commit()
        return {'message':'category deleted successfully'},200

class ProductResource(Resource):
    def get(self):
        categories = Category.query.all()
        categories_data = [{'id':category.id,'name':category.name}for category in categories]

        products = Product.query.all()
        products_data =[{
            'id':product.id,
            'name':product.name,
            'category_id':product.category_id,
            'expiry_date':product.expiry_date
        } for product in products]

        return jsonify({
            'categories':categories_data,
                        'products':products_data})


class PendingManager(Resource):
    def get(self):
        pending_managers=User.query.filter_by(approved=False,role='store-manager').all()
        pending_managers_data = []
        for manager in pending_managers:
            manager_data = {
                'id':manager.id,
                'name':manager.username,
                'email':manager.email,
            }
            pending_managers_data.append(manager_data)
        return jsonify(pending_managers_data)
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('manager_id',type=str,required=True)
        parser.add_argument('status',type=str,required=True)
        args= parser.parse_args()

        user = User.query.get(args['manager_id'])

        if not user:
            return {'message':'User not found'},404
        
        if args['status'] == 'approve':
            user.approved=True
        else:
            db.session.delete(user)
        db.session.commit()

        return {'message':'task completed succesffully'},200

class ExportResource(Resource):
    @jwt_required()
    def post(self,user_id):
        user_role = get_jwt_identity()
        if user_role !='admin':
            return jsonify({'message':'access deneid'})
        try:
            from tasks import export_categories_details_as_csv

            csv_data = export_categories_details_as_csv(user_id)

            response = make_response(csv_data)

            response.headers['Content-Disposition'] = 'attachment;filename=category_report.csv'

            response.headers['Content-type'] = 'text/csv'

            return response
        except Exception as e:
            return jsonify(e),500


api.add_resource(ExportResource,'/exportcsv/<int:user_id>')
api.add_resource(PendingManager,'/api/managers')
api.add_resource(CategoryResource,'/api/category')
api.add_resource(UserInfo,'/api/userinfo')
api.add_resource(SignupResource,'/api/signup')
api.add_resource(LoginResource,'/api/login')

if __name__ =="__main__":
    app.run(debug=True)