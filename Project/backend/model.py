from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,unique=True,nullable =False)
    email = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String,nullable=False)
    role = db.Column(db.String,default='user')
    approved = db.Column(db.Boolean,default=False)

    def __repr__(self):
        return f'<User{self.username}>'
    
class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name= db.Column(db.Integer,nullable=False,unique=True)

    def __repr__(self):
        return f'<Category {self.name}>'
    

class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name= db.Column(db.Integer,nullable=False,unique=True)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    category = db.relationship('Category',backref=db.backref('products',lazy=True))
    expiry_date = db.Column(db.Date)


with app.app_context():
    db.create_all()

    if User.query.filter_by(username='admin').first() is None:
        admin_password = generate_password_hash('adminpassword')

        admin = User(username='admin',email='admin@grocery.com',password = admin_password,role='admin',approved=True)

        db.session.add(admin)
        db.session.commit()
    else:
        print('Admin Already Exists')


    if Category.query.count() == 0:
        fruits = Category(name='Fruits')
        vegetables = Category(name='Vegetables')

        db.session.add_all([fruits,vegetables])
        db.session.commit()
    else:
        print('Categories already exists')

    if Product.query.count() == 0:
        mango = Product(name='mango',category_id=1,expiry_date = datetime.today())

        db.session.add(mango)
        db.session.commit()
    else:
        print('product already exists')