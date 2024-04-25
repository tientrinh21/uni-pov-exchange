from flask import Flask, url_for
from flask_restful import Api, Resource, fields, marshal_with, reqparse, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from sqlalchemy import URL, create_engine, select, text
from flask_swagger_ui import get_swaggerui_blueprint
import requests

# loads the variables in the .env file so we can access them
load_dotenv()
# app instance
app = Flask(__name__)
CORS(app)
# we are gonna build a api
api = Api(app)

# Swagger setup - https://pypi.org/project/flask-swagger-ui/
# https://www.youtube.com/watch?v=AyyX9yM_OZk
SWAGGER_URL = ''  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/api_swagger_docs.json' # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "EduVenture Api Docs"
    }
)
app.register_blueprint(swaggerui_blueprint)


# DB setup
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

app.config["SQLALCHEMY_DATABASE_URI"] = url_object
db = SQLAlchemy(app)


# inspo: https://www.youtube.com/watch?v=GMppyAPbLYk

# Here we are just reflecting the database
# Should maybe be changed at a later date,
# when the database schema is mostly decided on
db.Model.metadata.reflect(bind=create_engine(url_object), schema=DB_NAME)


class CountryTable(db.Model):
    """deal with an existing table"""

    __table__ = db.Model.metadata.tables[f"{DB_NAME}.country_table"]


class InfoPageTable(db.Model):
    """deal with an existing table"""

    __table__ = db.Model.metadata.tables[f"{DB_NAME}.info_page_table"]


class UniversityTable(db.Model):
    """deal with an existing table"""

    __table__ = db.Model.metadata.tables[f"{DB_NAME}.university_table"]

    def __repr__(self):
        return f'<University {self.university_id} + {self.long_name}>'


class PartnerUniversitiesTable(db.Model):
    """deal with an existing table"""

    __table__ = db.Model.metadata.tables[f"{DB_NAME}.partner_universities_table"]


class UserTable(db.Model):
    """deal with an existing table"""

    __table__ = db.Model.metadata.tables[f"{DB_NAME}.user_table"]

    def __repr__(self):
        return f'<User {self.username}>'


class ExchangeUniversityTable(db.Model):
    """deal with an existing table"""

    __table__ = db.Model.metadata.tables[f"{DB_NAME}.exchange_university_table"]


# The above code should be changed to this
# Basically is the schema in a data base
# class User(db.Model):
#     __tablename__ = f"{DB_NAME}.user_table"
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
    "info_page_id": fields.String,
    "intro_text": fields.String,
    "intro_source": fields.String,
}

university_resource_fields = {
    "university_id": fields.String,
    "country_code": fields.String,
    "region": fields.String,
    "long_name": fields.String,
    "info_page_id": fields.String,
}

university_with_info_resource_fields = {
    "university_id": fields.String,
    "country_code": fields.String,
    "region": fields.String,
    "long_name": fields.String,
    "info_page_id": fields.String,
    "info_page_id": fields.String,
    "intro_text": fields.String,
    "intro_source": fields.String,
}

user_resource_fields = {
    "user_id": fields.String,
    "username": fields.String,
    "pwd": fields.String,
    "nationality": fields.String,
    "home_university": fields.String,
}

user_with_university_resource_fields = {
    "user_id": fields.String,
    "username": fields.String,
    "pwd": fields.String,
    "nationality": fields.String,
    "university_id": fields.String,
    "country_code": fields.String,
    "region": fields.String,
    "long_name": fields.String,
    "info_page_id": fields.String,
}

# How to query with SQLAlchemy
# https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/queries/


class UserRes(Resource):
    @marshal_with(user_resource_fields)
    def get(self, user_id):
        return db.get_or_404(UserTable, user_id, description=f"No user with the ID '{user_id}'.")

user_put_args = reqparse.RequestParser()
user_put_args.add_argument('user_id', type=str, help='User ID to create user')
user_put_args.add_argument('username', type=str, help='User name to create user')
user_put_args.add_argument('pwd', type=str, help='Password to create user')
user_put_args.add_argument('nationality', type=str, help='Natioinality of user')
user_put_args.add_argument('home_university', type=str, help='Home university of user')

user_update_args = reqparse.RequestParser()
user_update_args.add_argument('user_id', type=str, help='User ID to update user')
user_update_args.add_argument('username', type=str, help='User name to update user')
user_update_args.add_argument('pwd', type=str, help='Password to update user')
user_update_args.add_argument('nationality', type=str, help='Natioinality of user')
user_update_args.add_argument('home_university', type=str, help='Home university of user')

# user_del_args = reqparse.RequestParser()
# user_del_args.add_argument('user_id', type=str, help='User ID to update user')
# user_del_args.add_argument('username', type=str, help='User name to update user')
# user_del_args.add_argument('pwd', type=str, help='Password to update user')
# user_del_args.add_argument('nationality', type=str, help='Natioinality of user')
# user_del_args.add_argument('home_university', type=str, help='Home university of user')

class UsersAllRes(Resource):
    @marshal_with(user_resource_fields)
    def get(self):
        users = UserTable.query.order_by(UserTable.username).all()
        return [user for user in users], 200
    
    @marshal_with(user_resource_fields)
    def put(self):
        try:
            args = user_put_args.parse_args()
            # Create a new UserTable object and assign values from args
            new_user = UserTable(
                user_id=args['user_id'],
                username=args['username'],
                pwd=args['pwd'],
                nationality=args['nationality'],
                home_university=args['home_university']
            )  
            db.session.add(new_user)
            db.session.commit()
            print(new_user)
            return new_user, 200
        except Exception as e:
            print(str(e))
            abort(message=str(e), http_status_code=400)
        
    @marshal_with(user_resource_fields, 200)
    def patch(self):
        try:
            args = user_update_args.parse_args()
            user_id = args['user_id']
            # user = UserTable.query.get(user_id)
            user = db.get_or_404(UserTable, user_id, description=f"No user with the ID '{user_id}'.")
            # Update the user attributes if they are present in the args
            if 'username' in args:
                user.username = args['username']
            if 'pwd' in args:
                user.pwd = args['pwd']
            if 'nationality' in args:
                user.nationality = args['nationality']
            if 'home_university' in args:
                user.home_university = args['home_university']
            db.session.commit()
            return user, 200
        except Exception as e:   
            abort(message=str(e), http_status_code=400)
        
    # def delete(self):
    #     user_id = None
    #     try:
    #         print('a')
    #         args = user_del_args.parse_args()
    #         print('b')
    #         user_id = args['user_id']
    #         print('c')
    #         user = db.get_or_404(UserTable, user_id, description=f"No user with the ID '{user_id}'.")
    #         print('d')
    #         del user
    #         print('e')
    #         db.session.commit()
    #         return user, 200
    #     except Exception as e:
    #         abort(message=str(e), http_status_code=400)
    def delete(self):
        try:
            args = user_update_args.parse_args()
            user_id = args['user_id']
            user = db.get_or_404(UserTable, user_id, description=f"No user with the ID '{user_id}'.")
            db.session.delete(user)
            db.session.commit()
            return {"message": f"User with ID '{user_id}' deleted successfully"}, 200
        except Exception as e:
            abort(message=str(e), http_status_code=400)

class UniversityRes(Resource):
    @marshal_with(university_resource_fields)
    def get(self, university_id):
        return db.get_or_404(UniversityTable, university_id,  description=f"No university with the ID '{university_id}'.")
    
class UniversityWithInfoRes(Resource):
    @marshal_with(university_with_info_resource_fields)
    def get(self, university_id):
        sql_raw = "SELECT * FROM university_table JOIN info_page_table ON university_table.info_page_id = info_page_table.info_page_id WHERE university_table.university_id = :val"
        res = db.session.execute(text(sql_raw), {"val": university_id}).first()
        print(res)
        return res

class UserWithUniversityRed(Resource):
    @marshal_with(user_with_university_resource_fields)
    def get(self, user_id):
        sql_raw = "SELECT * FROM user_table JOIN university_table ON user_table.home_university = university_table.university_id WHERE user_table.user_id = :val"
        res = db.session.execute(text(sql_raw), {"val": user_id}).first()
        print(res)
        return res

class UniversityAllRes(Resource):
    @marshal_with(university_resource_fields)
    def get(self):
        unis = UniversityTable.query.order_by(UniversityTable.long_name).all()
        return [uni for uni in unis], 200

# register the resource at a certain route
api.add_resource(UserRes, "/api/users/<string:user_id>")
api.add_resource(UsersAllRes, "/api/users")
api.add_resource(UniversityRes, "/api/universities/<string:university_id>")
api.add_resource(UniversityWithInfoRes, "/api/universities/<string:university_id>/info")
api.add_resource(UniversityAllRes, "/api/universities")
api.add_resource(UserWithUniversityRed, "/api/users/<string:user_id>/uni")
# beware. The address should not end with a slash

if __name__ == "__main__":
    app.run(debug=True, port=8080)
