from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from sqlalchemy import URL, create_engine, select, text

# loads the variables in the .env file so we can access them
load_dotenv()
# app instance
app = Flask(__name__)
CORS(app)
# we are gonna build a api
api = Api(app)

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_SERVER = os.getenv("DB_SERVER")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

url_object = URL.create(
    "mysql+mysqlconnector",
    username=DB_USERNAME,
    password=DB_PASSWORD,  # plain (unescaped) text
    host=DB_SERVER,
    port=DB_PORT,
    database=DB_NAME,
)

app.config['SQLALCHEMY_DATABASE_URI'] = url_object
db = SQLAlchemy(app)

# inspo: https://www.youtube.com/watch?v=GMppyAPbLYk

# Here we are just reflecting the database
# Should maybe be changed at a later date,
# when the database schema is mostly decided on
db.Model.metadata.reflect(bind=create_engine(url_object),schema=DB_NAME)
class CountryTable(db.Model):
    '''deal with an existing table'''
    __table__ = db.Model.metadata.tables[f'{DB_NAME}.countrytable']

class InfoPageTable(db.Model):
    '''deal with an existing table'''
    __table__ = db.Model.metadata.tables[f'{DB_NAME}.infopagetable']

class UniversityTable(db.Model):
    '''deal with an existing table'''
    __table__ = db.Model.metadata.tables[f'{DB_NAME}.universitytable']

class PartnerUniversitiesTable(db.Model):
    '''deal with an existing table'''
    __table__ = db.Model.metadata.tables[f'{DB_NAME}.partneruniversitiestable']

class UserTable(db.Model):
    '''deal with an existing table'''
    __table__ = db.Model.metadata.tables[f'{DB_NAME}.usertable']

class ExchangeUniversityTable(db.Model):
    '''deal with an existing table'''
    __table__ = db.Model.metadata.tables[f'{DB_NAME}.exchangeuniversitytable']

# The above code should be changed to this 
# Basically is the schema in a data base
# class User(db.Model):
#     user_id = db.Column(db.String(40), primary_key=True)
#     username = db.Column(db.String, unique=True)
#     # TODO: Handle password security
#     password = db.Column(db.String, nullable=False)
#     home_university = db.Column(db.String)

#     # to string
#     def __repr__(self):
#         return f'<User {self.username}>'
    
# handle serialization
info_page_resource_fields = {
    'info_page_id': fields.String,
    'intro_text': fields.String,
    'intro_source': fields.String
}

university_resource_fields = {
    'university_id': fields.String,
    'country_code': fields.String,
    'region': fields.String,
    'long_name': fields.String,
    'info_page_id': fields.String,
}

university_with_info_resource_fields = {
    'university_id': fields.String,
    'country_code': fields.String,
    'region': fields.String,
    'long_name': fields.String,
    'info_page_id': fields.String,
    'info_page_id': fields.String,
    'intro_text': fields.String,
    'intro_source': fields.String
}

user_resource_fields = {
    'user_id': fields.String, 
    'username': fields.String,
    'pwd': fields.String,
    'nationality': fields.String,
    'home_university': fields.String
}

user_with_university_resource_fields = {
    'user_id': fields.String, 
    'username': fields.String,
    'pwd': fields.String,
    'nationality': fields.String,
    'university_id': fields.String,
    'country_code': fields.String,
    'region': fields.String,
    'long_name': fields.String,
    'info_page_id': fields.String,
}


# How to query with SQLAlchemy
# https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/queries/

class UserRes(Resource):
    @marshal_with(user_resource_fields)
    def get(self, user_id):
        return db.get_or_404(UserTable, user_id)

class UsersAllRes(Resource):
    @marshal_with(user_resource_fields)
    def get(self):
        users = UserTable.query.order_by(UserTable.username).all()
        return [user for user in users], 200

class UniversityRes(Resource):
    @marshal_with(university_resource_fields)
    def get(self, university_id):
        return db.get_or_404(UniversityTable, university_id)
    
class UniversityWithInfoRes(Resource):
    @marshal_with(university_with_info_resource_fields)
    def get(self, university_id):
        sql_raw = 'SELECT * FROM universitytable JOIN infopagetable ON universitytable.info_page_id = infopagetable.info_page_id WHERE universitytable.university_id = :val'
        res =  db.session.execute(text(sql_raw), {"val": university_id}).first()
        print(res)
        return res

class UserWithUniversityRed(Resource):
    @marshal_with(user_with_university_resource_fields)
    def get(self, user_id):
        sql_raw = 'SELECT * FROM usertable JOIN universitytable ON usertable.home_university = universitytable.university_id WHERE usertable.user_id = :val'
        res =  db.session.execute(text(sql_raw), {"val": user_id}).first()
        print(res)
        return res
class UniversityAllRes(Resource):
    @marshal_with(university_resource_fields)
    def get(self):
        unis = UniversityTable.query.order_by(UniversityTable.long_name).all()
        return [uni for uni in unis], 200
    
# register the resource at a certain route
api.add_resource(UserRes, '/api/users/<string:user_id>')
api.add_resource(UsersAllRes, '/api/users')
api.add_resource(UniversityRes, '/api/university/<string:university_id>')
api.add_resource(UniversityWithInfoRes, '/api/university/<string:university_id>/info')
api.add_resource(UniversityAllRes, '/api/university')
api.add_resource(UserWithUniversityRed, '/api/users/<string:user_id>/uni')
# beware. The address should not end with a slash

if __name__ == "__main__":
    app.run(debug=True, port=8080)
